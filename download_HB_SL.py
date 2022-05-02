import os
import docker
from git import Repo
import json
import shutil
REPO_FOLDER = 'deployment'


# kILLING ALREADY running processes
import os, signal
  
def kill_process(name):
    try:
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
        print("Process Successfully terminated")        
    except:
        print("Error Encountered while running script")




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
# navigate to monitoring and run heartbeat processo 
# navigate and start server_lifecycle.py

print(cwd)
print("Setting up VMs")
os.system("echo 'setting vm' > vm_setup.txt ")
os.system("python3 setup_VM.py &")

print("Starting Server lifecycle")
os.system("echo 'setting lifecycle' > lifcycle_setup.txt ")

kill_process("server_lifecycle.py")
kill_process("heartbeat_processor.py")

os.system("python3 server_lifecycle.py & > /dev/null ; cd monitoring/ ; python3 heartbeat_processor.py & > /dev/null; logout")

