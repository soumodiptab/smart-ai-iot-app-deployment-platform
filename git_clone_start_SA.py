import os
import signal
import docker
import time
from git import Repo
import json
import shutil
import threading
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

os.system("./stop_docker.sh")


# os.system("cd service_agent ; python3 service_agent.py & > /dev/null ; cd /node_manager/node-agent ; python3 node_agent.py & > /dev/null")
# kill_process("service_agent.py")
# kill_process("node_agent.py")
# kill_process("app_deployment_consumer.py")

os.chdir(cwd)


def start_NA():
    node_agent_dir = cwd + "/node_manager/node-agent"
    os.chdir(node_agent_dir)
    os.system("echo 'node_agent_dir {}' > start_NA.txt".format(node_agent_dir))
    out = os.popen("python3 node_agent.py  & > /dev/null")
    os.system("echo 'node_agent_dir {} \n {}' > start_NA.txt".format(node_agent_dir, out))


def start_SA():
    service_agent_dir = cwd + "/service_agent"
    os.chdir(service_agent_dir)
    os.system("echo 'service_agent_dir {}' > start_SA.txt".format(service_agent_dir))
    os.system("python3 service_agent.py & > /dev/null")

def start_app_consumer():
    node_agent_dir = cwd + "/node_manager/node-agent"
    os.chdir(node_agent_dir)
    os.system("echo 'node_agent_dir {}' > start_app_dep.txt".format(node_agent_dir))
    os.system("python3 app_deployment_consumer.py  & > /dev/null")


t1 = threading.Thread(target=start_NA)
t2 = threading.Thread(target=start_SA)
t3 = threading.Thread(target=start_app_consumer)


t1.start()
time.sleep(2)
t3.start()
time.sleep(2)
t2.start()