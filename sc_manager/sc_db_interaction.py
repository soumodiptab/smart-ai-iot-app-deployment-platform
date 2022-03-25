
from logging import Logger
import logging
from pathlib import Path
from pymongo import MongoClient
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator
import glob
log = logging.getLogger('demo-logger')

# client -> sc_db -> sc_type | sc_instance
# sc_db = client["sc_db"]
# sc_type = sc_db["sc_type"]
# sc_instance = sc_db["sc_instance"]

# json schema for config file
# validator = Draft7Validator(sensor_type_schema)


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
            controller = json_config_loader(controller_file)
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
        for sensor_file in sensor_list:
            sensor = json_config_loader(sensor_file)
            errors = validate_object(sensor, sc_instance_schema)
            for error in errors:
                log.error(error)
                return False       
            if not insert_sc_instance_record(sensor):
                return False
        # iterate controllers and load json files in dict
        for controller_file in controller_list:
            controller = json_config_loader(controller_file)
            controller["device"] = "CONTROLLER"
            errors = validate_object(controller, sc_instance_schema)
            for error in errors:
                log.error(error)
                return False
            if not insert_sc_type_record(sc_instance_schema):
                return False
            return True
    pass


def insert_sc_type_record(sc_type_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_type.count_documents(sc_type_record):
        log.info(f'{sc_type_record} already present')
        return False
    client.sc_db.sc_type.insert_one(sc_type_record)
    client.close()
    return True


def insert_sc_instance_record(sc_instance_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_instance.count_documents(sc_instance_record) > 0:
        log.info(f'{sc_instance_record} already present')
        return False
    client.sc_db.sc_instance.insert_one(sc_instance_record)
    client.close()
    return True


def app_sc_type_map(message):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    application_uuid = message["app_id"]
    sensors = message["sensors"]
    controllers = message["controllers"]
    for sensor in sensors:
        sensor
    pass


def app_sc_instance_map(message):
    pass
    # sc_type_schema = {
    #     "company": "string",
    #     "model": "string",
    #     "parameter_count": 2,
    #     "parameters": [
    #         "int",
    #         "float"
    #     ]
    # }

    # insert_sc_type_record({
    #     "company": "QUALCOMM",
    #     "model": "AX123",
    #     "parameter_count": 2,
    #     "parameters": [
    #         "int",
    #         "float"
    #     ]
    # })
    # insert_sc_instance_record({

    # })
