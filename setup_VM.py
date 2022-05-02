import os
# from azure.identity import DefaultAzureCredential
import time
import paramiko
import docker
import pymongo
import shutil
from pymongo import MongoClient
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



ips = ["104.211.205.232","52.172.3.77", "104.211.227.22"]
count=1
for i in ips:
    print(f"Setting up VM :{i}")
    start_SA(i)
    os.system("echo 'setting up vm on {}' >> set_vm_ip.txt".format(i))
    time.sleep(5)
    data = {
        "service": "node-agent{}".format(count),
        "ip": i,
        "port": "5001",
        "port_status": "1",
        "type":"node-agent"
    }
    rec_id1 = collection.insert_one(data)
    count+=1