import requests
import datetime
import random
import json
import pickle

class Tripler(object):

    def get_random_resource(self, what=None):
        if what is None:
            resource_list = ["dataset", "campaign", "site", "aggregator", "calculator", "dimension", "dataset", "dataset"]
        else:
            resource_list = [what]
        
        resource = random.choice(resource_list)
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}

        req = s.get("http://localhost/api/v1/%s/"%resource, headers=headers)
        
        jresponse = json.loads(req.text)

        #print "total_count", jresponse["meta"]["total_count"] 
        #print "limit", jresponse["meta"]["limit"]

        total_count = jresponse["meta"]["total_count"]
        if total_count == 1:
            offset = 0
        elif total_count == 0:
            return self.get_random_resource()
        else:
            offset = random.choice(range(total_count - 1))

        print offset, "http://localhost/api/v1/%s/?offset=%s" % (resource, offset)

        req = s.get("http://localhost/api/v1/%s/?offset=%s" % (resource,offset), headers=headers)
        jresponse = json.loads(req.text)
        try:        
            chosen_resource = random.choice(jresponse["objects"])["resource_uri"]
            if what == "dataset":
                chosen_resource = random.choice(jresponse["objects"])
        except Exception:
            return self.get_random_resource()

        return chosen_resource
        

    def run(self):
        
        #get 3 resources random
        subject = self.get_random_resource()
        predicate = self.get_random_resource()
        obj = self.get_random_resource()
        
#        return
        payload = {}
        payload["subject"] = subject
        payload["predicate"] = predicate
        payload["object"] = obj
        payload["context"] = "/api/v1/graph/1/"
        payload = json.dumps(payload)
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}
        #insert
        req = s.post("http://localhost/api/v1/triple/", data=payload, headers=headers)
        if req.status_code == 500:
            print "error inserting"
        
        #print req.status_code, req.text
        #TODO on wsep API
        #will return 500 response if triple already exists
        
        #search triple
        directory = {"subject":subject,"predicate":predicate,"object":obj}
        
        choice = random.choice(directory.keys())
        #print "http://localhost/api/v1/triple/?%s=%s" % (choice, directory[choice])
        #print choice, directory.keys()
        print subject, predicate, obj
        for c in directory.keys():
            req = s.get("http://localhost/api/v1/triple/?%s=%s" % (c, directory[choice]), data=payload, headers=headers)
            print req.status_code,
        print
        
        
if __name__ == "__main__":
    t = Tripler()
    while True:
        t.run()
