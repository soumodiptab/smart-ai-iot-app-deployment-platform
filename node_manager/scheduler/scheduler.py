import os
import pymongo
import logging
import configparser
import time
import yaml
import json
from kafka import KafkaConsumer

from crontab import CronTab
from generate_cron import addToCron
from bson.objectid import ObjectId

cron = CronTab(user="vishal")

config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

db=cfg["mongo"]["db"]
collection= cfg["mongo"]["collection"]

connection_url="mongodb://" + cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)
database_name = db
app_info = client[database_name]
collections=app_info[collection]

# update_values = { "$set": { "active": "0" } }

# while(True):
#     # print("polling")
#     cursor = collections.find({"active": "1"})
#     # print(cursor)
#     for doc in cursor:
#         print(doc['_id'])
#         update_query = { "_id": ObjectId(doc['_id']) }
#         addToCron(doc)

#         collections.update_one(update_query, update_values)
#         time.sleep(10)

topic = cfg["kafka"]["topic"]
print(topic)
print(cfg["kafka"]["servers"])
sc_consumer = KafkaConsumer(
    topic,
    group_id=cfg["kafka"]["group"],
    bootstrap_servers=cfg["kafka"]["servers"],)
for msg in sc_consumer:
    print(msg.value)
    deployment_msg_from_deployer = json.loads(msg.value.decode('utf-8'))
    addToCron(deployment_msg_from_deployer, config_file)
    # startAppDeployment(deployment_msg_from_deployer)