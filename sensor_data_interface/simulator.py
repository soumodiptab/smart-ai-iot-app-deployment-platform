import logging
import os
from platform_logger import get_logger
from kafka import KafkaConsumer
import json
import glob
from utils import send_message
from utils import json_config_loader
import interfaces
from pymongo import MongoClient
from bson import ObjectId
import atexit
KAFKA_SERVERS = json_config_loader(
    'config/kafka.json')["bootstrap_servers"]
MONGODB_URL = json_config_loader('config/db.json')['DATABASE_URI']
log = get_logger('sc_data_interface', KAFKA_SERVERS)
sc_consumer = KafkaConsumer(
    "sc_data_interface",
    group_id='simulator',
    bootstrap_servers=KAFKA_SERVERS,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
global_directory = {}

image_folder = 'images'
device_settings = json_config_loader('config/sc_config.json')


def start_sc(sc):
    global global_directory
    client = MongoClient(MONGODB_URL)
    sc_details = client.sc_db.sc_instance.find_one(
        {"_id": ObjectId(sc["_id"])})
    if sc_details["status"] == "online":
        log.info('Device is already running')
        client.close()
        return
    device = sc_details["device"]
    type = sc_details["type"]
    ip_port = sc_details["ip_loc"]["ip"]+":"+sc_details["ip_loc"]["port"]
    try:
        if type not in device_settings.keys():
            expression = 'interfaces.'+type + \
                '('+'\"'+sc["_id"]+'\",'+'\"'+ip_port+'\")'
        else:
            latency = device_settings[type]['latency']
            expression = 'interfaces.'+type + \
                '('+'\"'+sc["_id"]+'\",'+'\"'+ip_port+'\"'+','+str(latency)+')'
        dev = eval(expression)
    except:
        log.error(f'device not available: {device}:{type}:{ip_port}')
        return
    if type == 'IMAGE':
        record = client.sc_db.sc_instance.find_one(
            {"_id": sc_details["_id"], "data_source": {"$exists": "true"}})
        if record == None:
            img_folder_loc = os.path.join(image_folder, 'default')
            log.error(f'Image folder not set for: {ip_port}::{device}')
        else:
            img_folder_loc = os.path.join(
                image_folder, sc_details["data_source"])
        if not os.path.exists(img_folder_loc):
            dev.set_data_source(os.path.join(image_folder, 'default'))
        else:
            dev.set_data_source(img_folder_loc)
    dev.start()
    global_directory[dev.id] = dev
    client.sc_db.sc_instance.update_one(
        {"_id": sc_details["_id"]}, {"$set": {"status": "online"}})
    log.info(f'Device:{type} :: {type} :: {ip_port} is up and running')
    client.close()


def stop_sc(sc):
    global current_image_folder
    global global_directory
    client = MongoClient(MONGODB_URL)
    sc_details = client.sc_db.sc_instance.find_one(
        {"_id": ObjectId(sc["_id"])})
    device = sc_details["device"]
    type = sc_details["type"]
    ip_port = sc_details["ip_loc"]["ip"]+":"+sc_details["ip_loc"]["port"]
    id = sc["_id"]
    try:
        if id not in global_directory:
            log.error(f'Device stop request issued but not present:{id}')
        else:
            dev = global_directory[id]
            dev.stop()
            global_directory.pop(id)
    except:
        log.error(f'device not available: {device}:{type}:{ip_port}')
        client.close()
        return
    client.sc_db.sc_instance.update_one(
        {"_id": sc_details["_id"]}, {"$set": {"status": "offline"}})
    client.close()


def init_instances():
    client = MongoClient(MONGODB_URL)
    sc_list = client.sc_db.sc_instance.find()
    for sc in sc_list:
        send_message("sc_data_interface", {
            "message_type": "SC_START",
            "_id": str(sc["_id"])
        })
    client.close()


def shutdown_instances():
    client = MongoClient(MONGODB_URL)
    sc_list = client.sc_db.sc_instance.find({"status": "online"})
    for sc in sc_list:
        send_message("sc_data_interface", {
            "message_type": "SC_STOP",
            "_id": str(sc["_id"])
        })
    client.close()


def cleanup_devices():
    for id in global_directory:
        global_directory[id].stop()
        client = MongoClient(MONGODB_URL)
        client.sc_db.sc_instance.update_one(
            {"_id": id}, {"$set": {"status": "offline"}})
    client.close()


if __name__ == "__main__":
    init_instances()
    atexit.register(cleanup_devices)
    for msg in sc_consumer:
        message_type = msg.value["message_type"]
        log.info(f"New sensor/controller request:{message_type}")
        if message_type == "SC_START":
            start_sc(msg.value)
        elif message_type == "SC_STOP":
            stop_sc(msg.value)
        else:
            log.info(f"Un-registered message :{message_type}")
