from platform_sdk import get_prediction, get_sensor_data, send_controller_data, get_sensor_image
import time
from pymongo import MongoClient
from platform_sdk import get_mongo_db_uri
from logging import Logger
import logging
log = logging.getLogger('demo-logger')
MONGO_DB_URL = get_mongo_db_uri()
#MONGO_DB_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_DB_URL)

db = client.model_stat
db.instance.insert_one({"modelId": "0", "class_0": 0,"class_1": 0,"class_2": 0,"class_3": 0, "class_4": 0})

c0=0
c1=0
c2=0
c3=0
c4=0
j = 0
d = {'Drizzle':0,'Fog':1, 'Rain':2,'Snow':3,'Sun':4}

while True:
    temp = get_sensor_data(0)
    pres = get_sensor_data(1)
    val = get_prediction(0, {
        "temp_max": temp,
        "perc": pres
    })
    if d[val] == 0:
        c0 += 1
        try:
            db.instance.update_one({"modelId": "0"}, {"$set": {"class_0": c0}})
        except Exception as e:
            log.error({'error': str(e)})

    elif d[val] == 1:
        c1 += 1
        try:
            db.instance.update_one({"modelId": "0"}, {"$set": {"class_0": c1}})
        except Exception as e:
            log.error({'error': str(e)})
    elif d[val] == 1:
        c2 += 1
        try:
            db.instance.update_one({"modelId": "0"}, {"$set": {"class_0": c2}})
        except Exception as e:
            log.error({'error': str(e)})
    elif d[val] == 1:
        c3 += 1
        try:
            db.instance.update_one({"modelId": "0"}, {"$set": {"class_0": c3}})
        except Exception as e:
            log.error({'error': str(e)})
    elif d[val] == 1:
        c4 += 1
        try:
            db.instance.update_one({"modelId": "0"}, {"$set": {"class_0": c4}})
        except Exception as e:
            log.error({'error': str(e)})
    j += 1

    # if (j == 100):
    #     break