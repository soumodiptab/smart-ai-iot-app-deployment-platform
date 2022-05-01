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


config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

log = get_logger('scheduler', cfg["kafka"]["address"])

cron = CronTab(user=cfg["cron"]["user"])
db=cfg["mongo"]["db"]
collection= cfg["mongo"]["collection"]

connection_url= cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)
database_name = db
app_info = client[database_name]
collections=app_info[collection]

topic = cfg["kafka"]["topic"]
print(topic)
print(cfg["kafka"]["address"])
sc_consumer = KafkaConsumer(
    topic,
    group_id=cfg["kafka"]["group"],
    bootstrap_servers=cfg["kafka"]["address"],)
for msg in sc_consumer:
    print(msg.value)
    deployment_msg_from_deployer = json.loads(msg.value.decode('utf-8'))
    addToCron(deployment_msg_from_deployer, config_file)
    # startAppDeployment(deployment_msg_from_deployer)
