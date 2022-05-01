# STEP 1:- Hit mongo db and get available ips
# STEP 2:- go on those ips and download(git clone) heartbeat processor and service lifecycle
# STEP 3:- install and run requirements
# STEP 4:- Install requirements and run Service agent on 3 VMs
# STEP 5:- get service names from json
# STEP 6:- Decide which service to run on which VM
# STEP 7:- Make an API to tell service agent as to which service to start

# from azure.storage.fileshare import ShareFileClient
import os
# from azure.identity import DefaultAzureCredential

import paramiko
import docker


import pymongo

# client = pymongo.MongoClient("mongodb://20.219.84.37:27017/")
# db = client["initialiser_db"]
# collection = db["available_vms"]


# Getting all avaiable ips
# available_ips = []
# for x in collection.find():
#   available_ips.append(x["ip"])


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
    "pip install kafka-python",
    "pip install dnspython",
    "pip install paramiko",
    "python3 download_HB_SL.py &",
]
host = "20.204.220.240"
user = "azureuser"
password = "password123@"
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, username=user, password=password)
sftp_client = ssh_client.open_sftp()
sftp_client.put('requirements.txt', 'requirements.txt')
sftp_client.put('git_credentials.json', 'git_credentials.json')
sftp_client.put('download_HB_SL.py', 'download_HB_SL.py')
sftp_client.close()
for command in exec_commands:
    _stdin, _stdout, _stderr = ssh_client.exec_command(command)
    print(_stdout.read().decode())
    print(_stderr.read().decode())
ssh_client.close()
