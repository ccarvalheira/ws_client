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
        pass
        #get 3 objects random
        subject = self.get_random_resource()
        predicate = self.get_random_resource()
        obj = self.get_random_resource()
        
        print subject, predicate, obj
        
        payload = {}
        payload["subject"] = subject
        payload["predicate"] = predicate
        payload["obj"] = obj
        payload = json.dumps(payload)
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}

        req = s.post("http://192.168.149.168/api/v1/triple/", data=payload headers=headers)
        print req.status
        
        
        
        #search triple 
