import requests
import datetime
import random
import json
import pickle


class Provider(object):

    def get_time(self, before):
        return before + datetime.timedelta(seconds=random.choice(xrange(2,5)))
            

    def run(self):
        s = requests.Session()

        headers = {'content-type': 'application/json'}

        with open("campaign.pck", "r") as f:
            new_campaign = pickle.loads(f.read())
        
        with open("c_dim.pck", "r") as f:
            c_dim = pickle.loads(f.read())

        with open("f_dim.pck", "r") as f:
            f_dim = pickle.loads(f.read())    
            
        with open("ctof.pck", "r") as f:
            ctof = pickle.loads(f.read())
        
        with open("ftok.pck", "r") as f:
            ftok = pickle.loads(f.read())
        
        with open("mean_2_sec.pck", "r") as f:
            mean_2_sec = pickle.loads(f.read())
        
        payload = {}
        payload["dimensions"] = [c_dim]
        payload["description"] = "medicoes de temperatura em C feitas na feup"
        payload["campaign"] = new_campaign
        payload["published"] = "false"
        payload["metadata"] = "cenas"
        payload["name"] = "medicoes C"
        payload["datapoint_count"] = 0
        payload = json.dumps(payload)

        req = s.post("http://192.168.149.168/api/v1/dataset/", data=payload, headers=headers)
        print req.status_code
        raw_dataset = req.headers["Location"].split("192.168.149.168")[1]
        print raw_dataset

        before = datetime.datetime.now()
        #days = random.choice(xrange(1,2))
        days = 0.1
        end_time = before + datetime.timedelta(seconds=days*86400) #number of seconds in a day
        while before < end_time:
            req.status_code = 1
            while req.status_code != 201:
                payload = {}
                payload["dataset"] = raw_dataset
                payload["dimensions"] = {}
                payload["dimensions"][c_dim] = random.choice(range(5,30))
                new_time = self.get_time(before)
                payload["dimensions"]["/api/v1/dimension/1/"] = "'"+str(new_time)+"'"
                before = new_time
                payload = json.dumps(payload)
                req = s.post("http://192.168.149.168/api/v1/datapoint/", data=payload, headers=headers)
            
                print req.status_code
                #print req.text
        
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

        req = s.post("http://192.168.149.168/api/v1/dataset/", data=payload, headers=headers)
        print req.status_code
        derived_dataset_f = req.headers["Location"].split("192.168.149.168")[1]
        print derived_dataset_f
        
        #ctof
        payload = {}
        payload["input_dataset"] = raw_dataset
        payload["output_dataset"] = derived_dataset_f
        payload["ordered_tasks"] = [mean_2_sec, ctof, ftok]
        payload = json.dumps(payload)

        req = s.post("http://192.168.149.168/api/v1/task/", data=payload, headers=headers)
        print req.text
        print "task"
        print req.status_code

