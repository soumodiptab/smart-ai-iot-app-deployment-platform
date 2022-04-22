import sys

from platform_logger import get_logger

config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

log = get_logger('app-stop-service', cfg["kafka"]["address"])

app_id = sys.argv[1]
app_instance_id = sys.argv[2]
isModel = sys.argv[3]
payload = {"app_id":app_id, "app_instance_id": app_instance_id, "isModel": isModel}
URL = "http://127.0.0.1:5005/deployer/deploy/stop"
response = requests.post(URL, data = payload)
print(response.json)