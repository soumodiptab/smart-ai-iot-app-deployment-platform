import json
import os
from pymongo import MongoClient


def json_config_loader(config_file_loc):
    print(os.getcwd())
    print(config_file_loc)
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data

MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
client = MongoClient(MONGO_DB_URL)
db = client["vm_details"]
my_collection = db["subsystem"]


def database_collection_drop():
    mydb = client["vm_details"]
    mycol = mydb["subsystem"]
    mycol.drop()

# Dropping the collection
database_collection_drop()
print("Dropped the collection subsystem")

# pushing the subsystem vm details in database 
file1 = open('vm_details.txt', 'r')
Lines = file1.readlines()
for line in Lines:
    line = line.strip()
    list = line.split(" ")
    for i in range(len(list)):
        list[i] = list[i].replace("'", "")
    print(list)
    
    data = {'ip': list[0], 'name': list[1], 'user': list[2]}
    my_collection.insert_one(data)
file1.close()





