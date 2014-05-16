import requests
import datetime
import random
import json
import pickle

s = requests.Session()

headers = {'content-type': 'application/json'}


#criar um site
payload = {}
payload["metadata"] = "cenas"
payload["location"] = "Porto, Portugal"
payload["description"] = "site fixe"
payload["name"] = "FEUP"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/site/", data=payload, headers=headers)
print req.status_code
#print req.text
new_site = req.headers["Location"].split("192.168.149.168")[1]
print new_site

with open("site.pck", "w") as f:
    f.write(pickle.dumps(new_site))
   


#criar uma campanha
payload = {}
payload["metadata"] = "cenas"
payload["location"] = "Porto, Portugal"
payload["description"] = "tese do Carlos"
payload["name"] = "Tese"
payload["site"] = new_site
payload["start_date"] = str(datetime.datetime.now())
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/campaign/", data=payload, headers=headers)
print req.status_code
new_campaign = req.headers["Location"].split("192.168.149.168")[1]
print new_campaign

with open("campaign.pck", "w") as f:
    f.write(pickle.dumps(new_campaign))


#criar dimensoes (nao esquecer criar tempo)
#cria-se tempo a partir do admin!!

#C
payload = {}
payload["units"] = "C"
payload["description"] = "temperatura em C"
payload["datatype"] = "Double"
payload["name"] = "Centigrade"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/dimension/", data=payload, headers=headers)
print req.text
print req.status_code
c_dim = req.headers["Location"].split("192.168.149.168")[1]
print c_dim

with open("c_dim.pck", "w") as f:
    f.write(pickle.dumps(c_dim))


#F
payload = {}
payload["units"] = "F"
payload["description"] = "temperatura em F"
payload["datatype"] = "Double"
payload["name"] = "Farenheit"
payload = json.dumps(payload)
    
req = s.post("http://192.168.149.168/api/v1/dimension/", data=payload, headers=headers)
print req.status_code
f_dim = req.headers["Location"].split("192.168.149.168")[1]
print f_dim

with open("f_dim.pck", "w") as f:
    f.write(pickle.dumps(f_dim))



#K
payload = {}
payload["units"] = "K"
payload["description"] = "temperatura em K"
payload["datatype"] = "Double"
payload["name"] = "Kelvin"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/dimension/", data=payload, headers=headers)
print req.status_code
k_dim = req.headers["Location"].split("192.168.149.168")[1]
print k_dim

with open("k_dim.pck", "w") as f:
    f.write(pickle.dumps(k_dim))


#criar duas calculator

#ctof
payload = {}
payload["output_dimension"] = f_dim
payload["input_dimensions"] = [c_dim]
payload["description"] = "converte C em F"
payload["custom_code"] = " "
payload["async_function"] = "ctof"
payload["metadata"] = "cenas"
payload["name"] = "C to F"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/calculator/", data=payload, headers=headers)
print req.status_code
ctof = req.headers["Location"].split("192.168.149.168")[1]
print ctof

with open("ctof.pck", "w") as f:
    f.write(pickle.dumps(ctof))


#ftok
payload = {}
payload["output_dimension"] = k_dim
payload["input_dimensions"] = [f_dim]
payload["description"] = "converte F em K"
payload["custom_code"] = " "
payload["async_function"] = "ftok"
payload["metadata"] = "cenas"
payload["name"] = "F to K"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/calculator/", data=payload, headers=headers)
print req.status_code
ftok = req.headers["Location"].split("192.168.149.168")[1]
print ftok

with open("ftok.pck", "w") as f:
    f.write(pickle.dumps(ftok))


#criar um aggregator
payload = {}
payload["interval_in_seconds"] = 20
payload["description"] = "faz media de 2 segundos"
payload["async_function"] = "mean"
payload["metadata"] = "cenas"
payload["name"] = "Media 2 segundos"
payload = json.dumps(payload)

req = s.post("http://192.168.149.168/api/v1/aggregator/", data=payload, headers=headers)
print req.status_code
mean_2_sec = req.headers["Location"].split("192.168.149.168")[1]
print mean_2_sec

with open("mean_2_sec.pck", "w") as f:
    f.write(pickle.dumps(mean_2_sec))

