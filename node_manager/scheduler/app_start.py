import sys
import requests
import yaml
import os
import yaml
from crontab import CronTab
from platform_logger import get_logger

config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

log = get_logger('app-start-service', cfg["kafka"]["address"])

def getServiceAddress(cfg, service_name):
	print("sending request to initialiser")
	URL = "http://" + cfg["initialiser"] + "/initialiser/getService/" + service_name
	r = requests.get(url = URL)
	data = r.json()
	ip = data["ip"]
	port = data["port"]

	address = ip + ":" + port
	return address


app_id = sys.argv[1]
app_instance_id = sys.argv[2]
isModel = sys.argv[3]

periodicity = sys.argv[4]
periodicity_unit = sys.argv[5]

config_file = sys.argv[6] + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

print(app_id, app_instance_id, isModel)

payload = {"app_id":app_id, "app_instance_id": app_instance_id, "isModel": isModel}
deployer_service_address = getServiceAddress(cfg, "deployer")
print(deployer_service_address)

URL = "http://" + deployer_service_address + "/deployer/deploy/start"
response = requests.post(URL, data = payload)
print(response.json)

start_script = sys.argv[6] + "/app_start.py"

my_cron = CronTab(user=cfg["cron"]["user"])

job1 = my_cron.new(command='/usr/bin/python3 ' + start_script + " "  + app_id + " " + app_instance_id + " " + isModel + " " +  "-1" + " " + periodicity_unit + " " + sys.argv[6])

if periodicity != "-1":
    if periodicity_unit == "Mins":
        job1.every(periodicity).min()

    if periodicity_unit == "Hrs":
        job1.every(periodicity).hour()
    my_cron.write()



#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
