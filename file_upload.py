import requests



s = requests.Session()

payload = {}
payload["name"] = "cenas"
payload["file_field"] = open("cli.py","r")

r = s.post("http://localhost:8001/api/v1/archive/", data=payload)

print r.text

