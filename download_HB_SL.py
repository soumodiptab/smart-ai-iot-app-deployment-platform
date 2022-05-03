import os
import docker
from git import Repo
import json
import shutil
import threading
import subprocess
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

cwd = os.getcwd()
os.environ["REPO_LOCATION"] = cwd


print("Setting up VMs")
os.system("echo 'setting vm' > vm_setup.txt ")
os.system("python3 setup_VM.py &")


kill_process("server_lifecycle.py")
kill_process("heartbeat_processor.py")



# def start_server_lifecycle():
    # os.system("python3 server_lifecycle.py & > /dev/null")

# def start_heartbeat():
    # heartbeat_dir = cwd + "/monitoring"
    # os.chdir(heartbeat_dir)
    # os.system("python3 heartbeat_processor.py & > /dev/null")

# t1 = threading.Thread(target=start_server_lifecycle)
# t2 = threading.Thread(target=start_heartbeat)

# t1.start()
# t2.start()

# subprocess.Popen(['gnome-terminal', '--', "python3",
                #  "server_lifecycle.py"], stdout=subprocess.PIPE)
subprocess.call(['gnome-terminal', "--", "python3", "server_lifecycle.py"])

heartbeat_dir = cwd + "/monitoring"
os.chdir(heartbeat_dir)

# subprocess.Popen(['gnome-terminal', '--', "python3",
#                  "heartbeat_processor.py"], stdout=subprocess.PIPE)
subprocess.call(['gnome-terminal', "--", "python3", "heartbeat_processor.py"])





