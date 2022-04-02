import os
import pymongo
import logging
import configparser

from crontab import CronTab
from generate_cron import addToCron


config = configparser.ConfigParser()
with open('scheduler_config.ini', 'w') as configfile:
    config.write(configfile)

connection_url="mongodb://" + config["mongo"]["ip"] + ":" + config["mongo"]["port"]
client=pymongo.MongoClient(connection_url)
database_name = config["mongo"]["db"]
app_info = client[database_name]

collection_name = config["mongo"]["collection"]
collection=app_info[collection_name]

cron = CronTab(user=config["cron"]["user"])

logging.basicConfig(filename='scheduler.log', filemode='w', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d-%b-%y %H:%M:%S')    

try:
    print("inside colection watch1")
    resume_token = None
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with collection.watch(pipeline) as stream:
        print("inside colection watch2")
        for insert_change in stream:
            print(insert_change["fullDocument"])
            generate_cron.addToCron(insert_change["fullDocument"])
            resume_token = stream.resume_token
except pymongo.errors.PyMongoError:
        with collection.watch(
                pipeline, resume_after=resume_token) as stream:
            for insert_change in stream:
                generate_cron.addToCron(insert_change["fullDocument"])

