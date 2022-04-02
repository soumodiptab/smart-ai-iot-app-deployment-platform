from flask import request
from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
import hashlib
import json
import requests


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


def get_sensor_data(sensor_index):
    """Get Sensor data by providing index mapped in config file

    Args:
        sensor_index (_type_): index in sensor config file

    Raises:
        Exception: SENSOR EXCEPTION

    Returns:
        _type_: sensor data
    """

    MONGO_IP_PORT = json_config_loader('config/db.json')["ip_port"]
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    log = get_logger(app_instance_id, kafka_servers)
    MONGO_DB_URL = f"mongodb://{MONGO_IP_PORT}/"
    client = MongoClient(MONGO_DB_URL)
    app_instance = client.app_db.instance.find_one(
        {"app_instance_id": app_instance_id})
    try:
        sensor_topic = app_instance["sensors"][sensor_index]
    except:
        log.error(f'Out of bounds sensor {sensor_index}')
        raise Exception('::: SENSOR EXCEPTION :::')
    client.close()

    try:
        consumer = KafkaConsumer(sensor_topic, group_id=app_instance_id, bootstrap_servers=kafka_servers,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for message in consumer:
            sensed_data = message.value['data']
            return sensed_data
    except:
        log.error(
            f'Error getting data from ::: {sensor_topic} for instance:{app_instance_id}')
        raise Exception('::: SENSOR EXCEPTION :::')

        # get info from sensor.json id -> type
        # sensor_type = json_config_loader(
        #     "config/sensors.json")["instances"]
        # # sensor type -> sensor instance
        # # generate app_id.jsonat the time of deployment
        # app_instance_id = json_config_loader("app_id.json")["app_id"]
        # MONGO_DB_URL = "mongodb://localhost:27017/"
        # client = MongoClient(MONGO_DB_URL)
        # client.sc_db.app_sc_bind.find({"app_instance_id": app_instance_id})
        # topic name - <ip-port>:<port>


def send_controller_data(controller_index, *args):
    """ Send data to controller using index

    Args:
        controller_index (_type_): index of controller

    Raises:
        Exception: _description_
    """
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    log = get_logger(app_instance_id, kafka_servers)
    MONGO_IP_PORT = json_config_loader('config/db.json')["ip_port"]
    MONGO_DB_URL = f"mongodb://{MONGO_IP_PORT}/"
    client = MongoClient(MONGO_DB_URL)
    app_instance = client.app_db.instance.find_one(
        {"app_instance_id": app_instance_id})
    try:
        controller_topic = app_instance["controllers"][controller_index]
    except:
        log.error(f'Out of bounds sensor {controller_index}')
        raise Exception('::: CONTROLLER EXCEPTION :::')
    client.close()
    try:
        producer = KafkaProducer(bootstrap_servers=kafka_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(controller_topic, {"data": args})
    except:
        log.error(
            f'Error sending data to ::: {controller_topic} for instance:{app_instance_id}')
        raise Exception('::: CONTROLLER EXCEPTION :::')


def get_prediction(model_index, json_obj):
    MONGO_IP_PORT = json_config_loader('config/db.json')
    MONGO_DB_URL = f"mongodb://{MONGO_IP_PORT}/"
    client = MongoClient(MONGO_DB_URL)
    # for counting hits(TODO)
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    models = json_config_loader('config/models.json')["instances"]
    model_id = models[model_index]
    ip_port = "127.0.0.1:9050"
    client.close()
    prediction_api = f"{ip_port}/predict/{model_id}"
    json_out = requests.post(prediction_api, json=json_obj).json()
    return json_out
