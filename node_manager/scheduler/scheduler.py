import os
import pymongo
import logging
import configparser
import time
import yaml
import json
import urllib.request

from kafka import KafkaConsumer
from crontab import CronTab
from generate_cron import addToCron
from bson.objectid import ObjectId
from platform_logger import get_logger
from heartbeat_client import HeartBeatClientForService


config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

log = get_logger('scheduler', cfg["kafka"]["address"])

cron = CronTab(user=cfg["cron"]["user"])
db=cfg["mongo"]["db"]
collection= cfg["mongo"]["collection"]
collection_1 = cfg["mongo"]["collection_1"]

connection_url= cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)
database_name = db
app_info = client[database_name]
collections=app_info[collection]
schedulable_collections = app_info[collection_1]

topic = cfg["kafka"]["topic"]
print(topic)
print(cfg["kafka"]["address"])
client = HeartBeatClientForService('scheduler')
client.start()
sc_consumer = KafkaConsumer(
    topic,
    group_id=cfg["kafka"]["group"],
    bootstrap_servers=cfg["kafka"]["address"],)
# for msg in sc_consumer:
#     print(msg.value)
#     deployment_msg_from_deployer = json.loads(msg.value.decode('utf-8'))
#     addToCron(deployment_msg_from_deployer, config_file)
    # startAppDeployment(deployment_msg_from_deployer)

pending_app_status = schedulable_collections.find({"app_schedule_status":"PENDING"})
for x in range(pending_app_status.count()):
	pending_msg_from_deployer = {}
	pending_msg_from_deployer["app_id"] = pending_app_status[x]["'app_id'"]
	pending_msg_from_deployer["app_instance_id"] = pending_app_status[x]["app_instance_id"]
	pending_msg_from_deployer["start_time"] = pending_app_status[x]["start_time"]
	pending_msg_from_deployer["end_time"] = pending_app_status[x]["end_time"]
	pending_msg_from_deployer["periodicity"] = pending_app_status[x]["periodicity"]
	pending_msg_from_deployer["periodicity_unit"] = pending_app_status[x]["periodicity_unit"]
	pending_msg_from_deployer["isModel"] = pending_app_status[x]["isModel"]
	addToCron(pending_msg_from_deployer, config_file)
	query = {"app_instance_id": pending_msg_from_deployer['app_instance_id']}
	update_values = {"$set":  {
	"app_schedule_status": "SCHEDULED"
	}}
	schedulable_collections.update_one(query, update_values)


for msg in sc_consumer:
    print(msg.value)
    deployment_msg_from_deployer = json.loads(msg.value.decode('utf-8'))
    if deployment_msg_from_deployer['app_instance_id']!=None:
	    query = {"app_instance_id": deployment_msg_from_deployer['app_instance_id']}
	    if query['app_schedule_status'] == "PENDING":
	    	addToCron(deployment_msg_from_deployer, config_file)
	    	update_values = {"$set":  {
	    	"app_instance_id": deployment_msg_from_deployer["app_instance_id"],
	    	"app_id":deployment_msg_from_deployer["app_id"],
	    	"start_time":deployment_msg_from_deployer["start_time"],
	    	"end_time":deployment_msg_from_deployer["end_time"],
	    	"periodicity":deployment_msg_from_deployer["periodicity"],
	    	"periodicity_unit":deployment_msg_from_deployer["periodicity_unit"],
	    	"isModel":deployment_msg_from_deployer["isModel"],
	    	"app_schedule_status": "SCHEDULED"
	    	}}
	        # schedulable_collections.update_one(query, update_values)
	    	schedulable_collections.update_one(query, update_values)
