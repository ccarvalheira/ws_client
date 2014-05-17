import requests
import datetime
import random
import json
import pickle

class Tripler(object):

    def get_random_resource(self):
        resource_list = ["dataset", "campaign", "site", "aggregator", "calculator", "dimension"]
        
        resource = random.choice(resource_list)
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}

        req = s.get("http://192.168.149.168/api/v1/%s/"%resource, headers=headers)
        
        jresponse = json.loads(req.text)
        
        chosen_resource = random.choice(jresponse["objects"])["resource_uri"]

        return chosen_resource
        

    def run(self):
        
        #get 3 resources random
        subject = self.get_random_resource()
        predicate = self.get_random_resource()
        obj = self.get_random_resource()
        
        print subject, predicate, obj
        
        payload = {}
        payload["subject"] = subject
        payload["predicate"] = predicate
        payload["object"] = obj
        payload["context"] = "/api/v1/graph/1/"
        payload = json.dumps(payload)
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}
        #insert
        req = s.post("http://192.168.149.168/api/v1/triple/", data=payload, headers=headers)
        
        print req.status_code, req.text
        #TODO on wsep API
        #will return 500 response if triple already exists
        
        #search triple
        directory = {"subject":subject,"predicate":predicate,"object":obj}
        
        choice = random.choice(directory.keys())
        #print "http://192.168.149.168/api/v1/triple/?%s=%s" % (choice, directory[choice])
        req = s.get("http://192.168.149.168/api/v1/triple/?%s=%s" % (choice, directory[choice]), data=payload, headers=headers)
        print req.status_code, req.text
        
        
        
t = Tripler()
while True:
    t.run()
