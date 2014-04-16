import requests
import datetime
import random
import json

s = requests.Session()

headers = {'content-type': 'application/json'}


#criar um site
payload = {}
payload["metadata"] = "cenas"
payload["location"] = "Porto, Portugal"
payload["description"] = "site fixe"
payload["name"] = "FEUP"
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/site/", data=payload, headers=headers)
print req.status_code
print req.text
new_site = req.headers["Location"].split("8001")[1]
print new_site


#criar uma campanha
payload = {}
payload["metadata"] = "cenas"
payload["location"] = "Porto, Portugal"
payload["description"] = "tese do Carlos"
payload["name"] = "Tese"
payload["site"] = new_site
payload["start_date"] = str(datetime.datetime.now())
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/campaign/", data=payload, headers=headers)
print req.status_code
new_campaign = req.headers["Location"].split("8001")[1]
print new_campaign


#criar dimensoes (nao esquecer criar tempo)
#cria-se tempo a partir do admin!!

#C
payload = {}
payload["units"] = "C"
payload["description"] = "temperatura em C"
payload["datatype"] = "Double"
payload["name"] = "Centigrade"
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/dimension/", data=payload, headers=headers)
print req.text
print req.status_code
c_dim = req.headers["Location"].split("8001")[1]
print c_dim

#F
payload = {}
payload["units"] = "F"
payload["description"] = "temperatura em F"
payload["datatype"] = "Double"
payload["name"] = "Farenheit"
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/dimension/", data=payload, headers=headers)
print req.status_code
f_dim = req.headers["Location"].split("8001")[1]
print f_dim

#K
payload = {}
payload["units"] = "K"
payload["description"] = "temperatura em K"
payload["datatype"] = "Double"
payload["name"] = "Kelvin"
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/dimension/", data=payload, headers=headers)
print req.status_code
k_dim = req.headers["Location"].split("8001")[1]
print k_dim


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

req = s.post("http://localhost:8001/api/v1/calculator/", data=payload, headers=headers)
print req.status_code
ctof = req.headers["Location"].split("8001")[1]
print ctof


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

req = s.post("http://localhost:8001/api/v1/calculator/", data=payload, headers=headers)
print req.status_code
ftok = req.headers["Location"].split("8001")[1]
print ftok


#criar um aggregator
payload = {}
payload["interval_in_seconds"] = 2
payload["description"] = "faz media de 2 segundos"
payload["async_function"] = "mean"
payload["metadata"] = "cenas"
payload["name"] = "Media 2 segundos"
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/aggregator/", data=payload, headers=headers)
print req.status_code
mean_2_sec = req.headers["Location"].split("8001")[1]
print mean_2_sec


#criar um dataset raw
payload = {}
payload["dimensions"] = [c_dim]
payload["description"] = "medicoes de temperatura em C feitas na feup"
payload["campaign"] = new_campaign
payload["published"] = "false"
payload["metadata"] = "cenas"
payload["name"] = "medicoes C"
payload["datapoint_count"] = 0
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/dataset/", data=payload, headers=headers)
print req.status_code
raw_dataset = req.headers["Location"].split("8001")[1]
print raw_dataset


if True:
    #inserir datapoints
    for x in xrange(300):
        req.status_code = 1
        while req.status_code != 201:
            payload = {}
            payload["dataset"] = raw_dataset
            payload["dimensions"] = {}
            payload["dimensions"][c_dim] = random.choice(range(5,30))
            payload["dimensions"]["/api/v1/dimension/1/"] = "'"+str(datetime.datetime.now())+"'"
            payload = json.dumps(payload)
            req = s.post("http://localhost:8001/api/v1/datapoint/", data=payload, headers=headers)
        
            print req.status_code
            print req.text
        #poi = req.headers["Location"].split("8001")[1]
        #print raw_dataset

#batch create datapoints
if False:
    payload = {}
    payload["objects"] = []
    for x in xrange(5):
        npayload = {}
        npayload["dataset"] = raw_dataset
        npayload["dimensions"] = {}
        npayload["dimensions"][c_dim] = random.choice(range(5,30))
        npayload["dimensions"]["/api/v1/dimension/1/"] = "'"+str(datetime.datetime.now())+"'"
        payload["objects"].append(npayload)

    sent_payload = json.dumps(payload)

    print "inserting datapoints"
    req = s.patch("http://localhost:8001/api/v1/datapoint/", data=sent_payload, headers=headers)

    print req.status_code
    print req.text


#criar dataset derivado
payload = {}
payload["dimensions"] = [f_dim]
payload["description"] = "medicoes de temperatura feitas na feup, convertidas para F"
payload["campaign"] = new_campaign
payload["published"] = "false"
payload["metadata"] = "cenas"
payload["name"] = "medicoes F derivadas"
payload["datapoint_count"] = 0
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/dataset/", data=payload, headers=headers)
print req.status_code
derived_dataset_f = req.headers["Location"].split("8001")[1]
print derived_dataset_f

#iniciar task

#ctof
payload = {}
payload["input_dataset"] = raw_dataset
payload["output_dataset"] = derived_dataset_f
payload["ordered_tasks"] = [mean_2_sec, ctof, ftok]
payload = json.dumps(payload)

req = s.post("http://localhost:8001/api/v1/task/", data=payload, headers=headers)
print req.text
print "task"
print req.status_code



#for i in xrange(3000):
#	now = datetime.datetime.now()
#	temp = random.choice(range(100))
#	press = random.choice(range(50,200))
#	payload = {}
#	payload["year"] = now.year
#	payload["month"] = now.month
#	payload["day"] = now.day
#	payload["hour"] = now.hour
#	payload["minute"] = now.minute
#	payload["second"] = now.second
#	payload["microsecond"] = now.microsecond
#	payload["data"] = {}
#	payload["data"]["humidade"] = press
#	payload["data"]["temperature"] = temp
#	payload["data"] = json.dumps(payload["data"])
#	r = s.post("http://localhost:8001/api/v1.0/insert/24", data=payload)
#	print r






	

