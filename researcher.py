import requests
import datetime
import random
import json
import pickle

from tripler import Tripler

class Researcher(object):

    time_interval = 30 #in seconds

    def get_random_dataset(self):
        t = Tripler()
        return t.get_random_resource("dataset")
        #return "cenas"
        #s = requests.Session()
        #headers = {'content-type': 'application/json'}

        #req = s.get("http://localhost/api/v1/dataset/", headers=headers)
        #print req.text
        #jresponse = json.loads(req.text)
        
        #chosen_resource = random.choice(jresponse["objects"])

        #return chosen_resource

    def run(self):
        #get random dataset
        
        dataset = self.get_random_dataset()
        
        
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        upper_bound = datetime.datetime.strptime(dataset["lowest_ts"], date_format) + datetime.timedelta(seconds=self.time_interval)
        
        print dataset["resource_uri"], dataset["lowest_ts"], upper_bound
        
        s = requests.Session()
        headers = {'content-type': 'application/json'}
        #read interval
        req = s.get("http://localhost%s?upper_time=%s" % (dataset["resource_uri"], str(upper_bound)), headers=headers)
        
        #print req.text
        
        
        #TODO
        #upload blob
        
        #consult blob
        
        #download blob


r = Researcher()
while True:
    r.run()
