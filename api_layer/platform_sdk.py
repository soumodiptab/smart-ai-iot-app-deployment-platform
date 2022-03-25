from utils import json_config_loader
from pymongo import MongoClient


def get_sensor_data(sensor_index):
    # get info from sensor.json id -> type
    sensor_type = json_config_loader(
        "config/sensors.json")["instances"]
    # sensor type -> sensor instance
    # generate app_id.jsonat the time of deployment
    app_instance_id = json_config_loader("app_id.json")["app_id"]
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    client.sc_db.app_sc_bind.find({"app_instance_id": app_instance_id})
    # topic name - <ip-port>
