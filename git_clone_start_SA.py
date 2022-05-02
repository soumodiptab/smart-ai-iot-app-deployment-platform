import os
import signal
import docker
from git import Repo
import json
import shutil
REPO_FOLDER = 'deployment'


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data

def kill_process(name):
    try:
        for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
            fields = line.split()
            pid = fields[0]
            os.kill(int(pid), signal.SIGKILL)
        print("Process Successfully terminated")        
    except:
        print("Error Encountered while running script")


kill_process("service_agent.py")
kill_process("node_agent.py")

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
cwd = os.getcwd()
os.environ["REPO_LOCATION"] = cwd

os.system("docker kill $(docker ps -q)")
os.system("docker rm $(docker ps -a -q)")
os.system("docker rmi $(docker images -q)")


# os.system("cd service_agent ; python3 service_agent.py & > /dev/null ; cd /node_manager/node-agent ; python3 node_agent.py & > /dev/null")

os.chdir(cwd)
os.system("chmod +x start_SA_NA.sh")
os.system("./start_SA_NA.sh")
