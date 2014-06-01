import requests
import time
import datetime

print "timestamp", "not_done", "all"
while True:
    s = requests.Session()

    req = s.get("http://localhost/task_counter/")
    counters = req.text.split(",")
    with open("tasks.log", "a") as f:
	f.write(str(datetime.datetime.now())+" - "+counters[0]+"\n")
    print datetime.datetime.now(), counters[0], counters[1]
    time.sleep(60)
