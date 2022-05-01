from platform_sdk import get_prediction, send_controller_data,get_sensor_image
import time
from pymongo import MongoClient
from platform_sdk import get_mongo_db_uri
from logging import Logger
import logging
log = logging.getLogger('demo-logger')
MONGO_DB_URL = get_mongo_db_uri()
client = MongoClient(MONGO_DB_URL)
db = client.model_stat
db.instance.insert_one({"modelId":"1","class_1":0,"class_0":0})
c1=0
c0=0
while True:
    stream=get_sensor_image(1)
    val=get_prediction(1,stream)
    if val == 1:
        c1+=1
        try:
            db.instance.update_one({ "modelId" : "1" },{ "$set": { "class_1" :c1} } )
        except Exception as e:
            log.error({'error': str(e)})

    else:
        c0+=1
        try:
            db.instance.update_one({ "modelId" : "1" },{ "$set": { "class_0" :c0} } )
        except Exception as e:
            log.error({'error': str(e)})


    send_controller_data(1,val)
    time.sleep(3)