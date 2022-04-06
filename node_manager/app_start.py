import sys
import requests

app_id = sys.argv[1]
app_instance_id = sys.argv[2]
isModel = sys.argv[3]
print(app_id, app_instance_id, isModel)
payload = {"app_id":app_id, "app_instance_id": app_instance_id, "isModel": isModel}
URL = "http://127.0.0.1:5002/deployer/deploy/start"
response = requests.post(URL, data = payload)
print(response.json)




