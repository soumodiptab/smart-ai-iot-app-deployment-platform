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


from pymongo import MongoClient

# client = pymongo.MongoClient("mongodb://20.219.84.37:27017/")
# db = client["initialiser_db"]
# collection = db["available_vms"]


# Getting all avaiable ips
# available_ips = []
# for x in collection.find():
#   available_ips.append(x["ip"])


print("Clearing DATABASE")

client = MongoClient(
    "mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

databases = client.list_database_names()

rm_database = ['admin', 'config', 'local', 'node_manager_db', 'initialiser_db']
databases_final = [
    db_name for db_name in databases if db_name not in rm_database]


for db_name in databases:
    if db_name == "startup_log" or db_name=="admin" or db_name=="local":
        continue
    print("deleting: ", db_name)
    current_db = client[db_name]
    collections = current_db.list_collection_names()

    for collection_name in collections:
        mycol = current_db[collection_name]
        mycol.drop()

database = client["intializer_db"]
collection = database["services"]


print("Populating initialiser DATABASE")

data1 = {
    "service": "node_manager",
    "dockerised": "1",
    "directory": "node_manager/node-manager",
    "port": "6501"
}
data2 = {
  "service": "ai_manager",
  "dockerised": "1",
  "directory": "ai_manager",
  "port": "6500"
}
data3 = {
    "service": "deployer",
  "dockerised": "1",
  "directory": "node_manager/deployer",
  "port": "6503"
}
data4 = {
    "service": "app_manager",
  "dockerised": "1",
  "directory": "app_manager",
  "port": "8200"
}
data5 = {
  "service": "scheduler",
  "dockerised": "1",
  "directory": "node_manager/scheduler",
  "port": "6505"
}
data6 = {
  "service": "request_manager",
  "dockerised": "1",
  "directory": "request_manager",
  "port": "8080"
}
data7 = {
  "service": "sc_manager",
  "dockerised": "1",
  "directory": "sc_manager",
  "port": "8101"
}
data8 = {
    "service": "email_notifier",
  "dockerised": "1",
  "directory": "email_notifier",
  "port": "6505"
}
rec_id1 = collection.insert_one(data1)
rec_id2 = collection.insert_one(data2)
rec_id3 = collection.insert_one(data3)
rec_id4 = collection.insert_one(data4)
rec_id5 = collection.insert_one(data5)
rec_id6 = collection.insert_one(data6)
rec_id7 = collection.insert_one(data7)
rec_id8 = collection.insert_one(data8)


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
    "pip install flask",
    "python3 download_HB_SL.py &",
]
host = "104.211.226.233"
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
