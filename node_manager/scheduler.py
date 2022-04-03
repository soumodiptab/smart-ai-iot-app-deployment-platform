import os
import pymongo
import logging
import configparser

from crontab import CronTab
from generate_cron import addToCron


config = configparser.ConfigParser()
config.read("scheduler_config.ini")

# mongo_ip = config['MONGO']['ip']
# port = config['MONGO']['port']
# db = config.get['MONGO']['db']

port=27017
db="scheduler_db"
collection="scheduler_metadata"

connection_url="mongodb://mongo-admin:iasproject@20.235.9.68:27017/?authSource='admin'"
client=pymongo.MongoClient(connection_url)
database_name = db
app_info = client[database_name]

# collection_name = config.get("MONGO", "collection")
collection=app_info[collection]

cron = CronTab(user="vishal")

#logging.basicConfig(filename='scheduler.log', filemode='w', 
#                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
#                  datefmt='%d-%b-%y %H:%M:%S')    

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
                print(insert_change["fullDocument"])
                # generate_cron.addToCron(insert_change["fullDocument"])

