import os
import pymongo
import logging
import configparser
import time
import yaml

config_file = os.environ.get("SCHEDULER_HOME") + "/watcher_config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

db=cfg["mongo"]["db"]
collection= cfg["mongo"]["collection"]

connection_url="mongodb://" + cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)
database_name = db
app_info = client[database_name]
collections=app_info[collection]

print(connection_url)
try:
    resume_token = None
    pipeline = [{'$match': {'operationType': 'insert'}}]
    with collections.watch(pipeline) as stream:
        for insert_change in stream:
            print(insert_change)
            resume_token = stream.resume_token
except Exception as e:
	print(e)
	if resume_token is None:
		print(pymongo.errors.PyMongoError)
	else:
		with db.collection.watch(
			pipeline, resume_after=resume_token) as stream:
			for insert_change in stream:
				print(insert_change)