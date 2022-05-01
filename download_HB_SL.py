import os
import docker
from git import Repo
import json
import shutil
REPO_FOLDER = 'deployment'


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data


print('[info]: Deleting previous deployment repository')
if os.path.exists(REPO_FOLDER):
    shutil.rmtree(REPO_FOLDER)
os.mkdir(REPO_FOLDER)
credentials = json_config_loader('git_credentials.json')
username = credentials["username"]
password = credentials["password"]
print('[info]: Downloading deployment package...')
remote = f"https://{username}:{password}@github.com/soumodiptab/smart-ai-iot-app-deployment-platform.git"
Repo.clone_from(remote, REPO_FOLDER)
# add deployment branch later on...
print('[info]: Deployment package downloaded...')
os.chdir(REPO_FOLDER)
# --------------------------------------------------
# print('Removing orphan containers')
# os.system('./docker_stop.sh')
# print('Starting all containers')
# os.system('./docker_initializer.sh')
# print('Started all containers')
cwd = os.getcwd()
os.environ["REPO_LOCATION"] = cwd
# navigate to monitoring and run heartbeat montitor and client
# navigate and start server_lifecycle.py

print(cwd)
print("Setting up VMs")
os.system("python3 setup_VM.py &")
heartbeart_dir = cwd+"/monitoring"
os.chdir(heartbeart_dir)
print("starting heartbeat processor")
os.system("chmod +x heartbeat_processor.py")
os.system("nohup heartbeat_processor.py &")
#os.system("./start.sh &")
os.chdir(cwd)
print("Starting Server lifecycle")
os.system("chmod +x server_lifecycle.py")
os.system("nohup server_lifecycle.py &")
os.system("python3 server_lifecycle.py &")
os.system("logout")
# in ubuntu
