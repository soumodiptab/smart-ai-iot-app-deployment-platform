from logging import Logger
import logging
from pathlib import Path
from platform_logger import get_logger
from pymongo import MongoClient
from utils import json_config_loader, get_file_name, validate_object, send_message
from zipfile import ZipFile
import glob
#log = get_logger('sensor_manager', 'localhost:9094')
log = get_logger('sensor_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
MONGO_DB_URL = json_config_loader('config/db.json')["DATABASE_URI"]


def validate_sc_type_and_insert(zip_file_loc):
    sc_type_schema = json_config_loader('config/sc_type_schema.json')
    # first extract zip
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)
        # get all sensors and controllers
        try:
            sensor_list = glob.glob(extract_path+"/sensor/*.json")
            controller_list = glob.glob(extract_path+"/controller/*.json")
        except:
            log.error('folder structure is incorrect')
            return False
        # iterate sensors and load json files in dict
        for sensor_file in sensor_list:
            sensor_type = get_file_name(sensor_file)
            sensor = json_config_loader(sensor_file)
            errors = validate_object(sensor, sc_type_schema)
            for error in errors:
                log.error(error)
                return False
            sensor["device"] = "SENSOR"
            sensor["type"] = sensor_type
            if not insert_sc_type_record(sensor):
                return False
        # iterate controllers and load json files in dict
        for controller_file in controller_list:
            controller = json_config_loader(controller_file)
            controller_type = get_file_name(controller_file)
            errors = validate_object(controller, sc_type_schema)
            for error in errors:
                log.error(error)
                return False
            controller["device"] = "CONTROLLER"
            controller["type"] = controller_type
            if not insert_sc_type_record(controller):
                return False
    return True


def validator_sc_instance_and_insert(zip_file_loc):
    sc_instance_schema = json_config_loader('config/sc_instance_schema.json')
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)
        # get all sensors and controllers
        try:
            sensor_list = glob.glob(extract_path+"/sensors/*.json")
            controller_list = glob.glob(extract_path+"/controllers/*.json")
        except:
            log.error('folder structure is incorrect')
            return False
        # iterate sensors and load json files in dict
        sc_list = []
        ip_port_checker = set()
        for sensor_file in sensor_list:
            sensor = json_config_loader(sensor_file)
            errors = validate_object(sensor, sc_instance_schema)
            for error in errors:
                log.error(error)
                return False
            sensor_type = sensor["type"]
            if not check_sc_type("SENSOR", sensor_type):
                return False
            if check_duplicate_sc_instance({"ip_loc": sensor["ip_loc"]}):
                return False
            ip_port = sensor["ip_loc"]["ip"]+"@"+sensor["ip_loc"]["port"]
            if ip_port in ip_port_checker:
                return False
            else:
                ip_port_checker.add(ip_port)
            sensor["device"] = "SENSOR"
            sc_list.append(sensor)
            # if not insert_sc_instance_record(sensor):
            #     return False
        # iterate controllers and load json files in dict
        for controller_file in controller_list:
            controller = json_config_loader(controller_file)
            errors = validate_object(controller, sc_instance_schema)
            for error in errors:
                log.error(error)
                return False
            controller_type = controller["type"]
            if not check_sc_type("CONTROLLER", controller_type):
                return False
            if check_duplicate_sc_instance({"ip_loc": controller["ip_loc"]}):
                return False
            ip_port = controller["ip_loc"]["ip"] + \
                "@"+controller["ip_loc"]["port"]
            if ip_port in ip_port_checker:
                return False
            else:
                ip_port_checker.add(ip_port)
            controller["device"] = "CONTROLLER"
            sc_list.append(controller)
            # if not insert_sc_instance_record(controller):
            #     return False
        errors = []
        for sc in sc_list:
            sc['status'] = 'online'
            if not insert_sc_instance_record(sc):
                errors.append(sc['device'])
            log.info(f"New device registered: {sc}")
            client = MongoClient(MONGO_DB_URL)
            id = str(client.sc_db.sc_instance.find_one(sc)['_id'])
            sc_topic = "START_"+sc["ip_loc"]["ip"]+"_"+sc["ip_loc"]["port"]
            send_message(sc_topic,
                         {
                             "message_type": "SC_START"
                         })
    return True


def check_duplicate_sc_instance(query):
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_instance.count_documents(query) > 0:
        log.info(f'{query} already present')
        return True
    client.close()
    return False


def insert_sc_type_record(sc_type_record):
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_type.count_documents(sc_type_record) > 0:
        log.info(f'{sc_type_record} already present')
        return True
    client.sc_db.sc_type.insert_one(sc_type_record)
    client.close()
    return True


def insert_sc_instance_record(sc_instance_record):
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_instance.count_documents(sc_instance_record) > 0:
        log.info(f'{sc_instance_record} already present')
        return False
    client.sc_db.sc_instance.insert_one(sc_instance_record)
    client.close()
    return True


def app_sc_type_map(message):
    client = MongoClient(MONGO_DB_URL)
    application_uuid = message["app_id"]
    sensors = message["sensors"]
    controllers = message["controllers"]
    for sensor in sensors:
        sensor
    client.close()
    pass


def check_sc_type(device, sc_type):
    client = MongoClient(MONGO_DB_URL)
    if not client.sc_db.sc_type.count_documents({"device": device, "type": sc_type}) > 0:
        log.info(f'Device: {device} Type:{sc_type} not present in Platform')
        return False
    client.close()
    return True

    # sc_type_schema = {
    #     "company": "string",
    #     "model": "string",
    #     "parameter_count": 2,
    #     "parameters": [
    #         "int",
    #         "float"
    #     ]
    # }

    # insert_sc_instance_record({

    # })
# insert_sc_type_record({
#     "company": "QUALCOMM",
#     "model": "AX123",
#     "parameter_count": 2,
#     "parameters": [
#         "int",
#         "float"
#     ]
# })
