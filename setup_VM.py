import os
# from azure.identity import DefaultAzureCredential
import time
import paramiko
import docker
import pymongo
import shutil
from pymong import MongoClient
# --------------------------------------------------

client = MongoClient(
    "mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


cwd = os.getcwd()
os.environ["REPO_LOCATION"] = cwd
def start_SA(ip):
    exec_commands = [
        "sudo apt update -y &",
        "sudo apt upgrade -y &",
        "sudo add-apt-repository universe &",
        "sudo apt-get update -y &"
        "sudo apt-get install python3.8 &",
        "sudo apt install -y build-essential libssl-dev libffi-dev python3-dev -y &",
        "sudo apt install python3-pip -y & "
        "sudo apt-get install git &",
        "pip install -r requirements.txt &",
        "pip install docker &",
        "sudo apt-get install python3-git -y &",
        "pip install gitpython",
        "pip install pymongo",
        "pip install psutil",
        "pip install kafka-python",
        "pip install dnspython",
        "sudo chmod 777 /var/run/docker.sock",
        "python3 git_clone_start_SA.py &",
        "logout"
    ]
    host = ip
    user = "azureuser"
    password = "password123@"
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, username=user, password=password)
    sftp_client = ssh_client.open_sftp()
    sftp_client.put('requirements.txt', 'requirements.txt')
    sftp_client.put('git_credentials.json', 'git_credentials.json')
    sftp_client.put('git_clone_start_SA.py', 'git_clone_start_SA.py')
    sftp_client.close()
    for command in exec_commands:
        _stdin, _stdout, _stderr = ssh_client.exec_command(command)
        # print(_stdout.read().decode())
        # print(_stderr.read().decode())
    ssh_client.close()



database = client["initialiser_db"]
collection = database["running_services"]



ips = ["20.207.107.115","20.204.220.249"]
count=1
for i in ips:
    print(f"Setting up VM :{i}")
    start_SA(i)
    time.sleep(5)
    data = {
        "service": "node-agent{}".format(count),
        "ip": i,
        "port": "5001",
        "port_status": "1",
        "type":"node-agent"
    }
    count+=1