import os
import json
from genericpath import isfile
from logging import Logger
import logging
from pathlib import Path
from pymongo import MongoClient
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator

#from jsonschema import validate
import glob
log = logging.getLogger('demo-logger')

# zip_file_loc="/home/sourav/IIITH/app.zip"


def validate_app_and_insert(zip_file_loc):
    #control_schema = json_config_loader('config/control.json')
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)
        # print(extract_path)
        # get all sensors and controllers

    f = open(extract_path+'/app.json')
    data = json.load(f)
    if(data['scripts']):
        control1 = json_config_loader(
            extract_path+'/config/control.json')  # json_file
        f1 = open(extract_path+'/config/control.json')
        data1 = json.load(f1)
        control = json_config_loader(
            'config/control_schema.json')  # json_schema
        errors = validate_object(control1, control)
        if not errors:
            for script in data1['scripts']:
                path = extract_path+'/'+script['filename']
                # print(path)
                if(os.path.isfile(path)):
                    print(isfile)
                else:
                    return False

    if(data['controllers']):
        control1 = json_config_loader(extract_path+'/config/controllers.json')
        control = json_config_loader('config/controllers_schema.json')
        errors = validate_object(control1, control)
        if not errors:
            f = open(extract_path+'/config/models.json')
            control_req = json.load(f)
            client = MongoClient()
            client = MongoClient("mongodb://localhost:27017/")
            for controllers in control_req['instances']:
                ctrl_type = controllers['type']
                if client.sc_db.sc_type.count_documents({"type": ctrl_type,  "device": "CONTROLLER"}) > 0:
                    print("controllers found")
                else:
                    return False
            client.close()

    if(data['models']):
        control1 = json_config_loader(extract_path+'/config/models.json')
        control = json_config_loader('config/models_schema.json')
        errors = validate_object(control1, control)
        if not errors:
            f = open(extract_path+'/config/models.json')
            model_req = json.load(f)
            client = MongoClient()
            client = MongoClient("mongodb://localhost:27017/")
            for models in model_req['instances']:
                model_id = models['model_id']
                if client.ai_data.model_info.count_documents({'modelId': model_id}) > 0:
                    print("Model doesn't exist")
                else:
                    print("Model exists")
                    return False
            client.close()

    if(data['sensors']):
        control1 = json_config_loader(extract_path+'/config/sensors.json')
        control = json_config_loader('config/sensors_schema.json')
        errors = validate_object(control1, control)
        if not errors:
            f = open(extract_path+'/config/sensors.json')
            sensors_req = json.load(f)
            client = MongoClient()
            client = MongoClient("mongodb://localhost:27017/")
            for sensors in sensors_req['instances']:
                sensors_type = sensors['type']
                if client.sc_db.sc_type.count_documents({"type": sensors_type, "device": "SENSOR"}) > 0:
                    print("sensors exist")
                else:
                    return False
            client.close()

    return True

# validate_app_and_insert(zip_file_loc)


def validate_app_instance(app_config):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    app = client.app_db.app.find({"app_id": app_config["app_id"]})[0]
    for instance in app_config["instances"]:
        sc_list = client.sc_db.sc_instance.find(
            {"geo_location": instance["geo_loc"]})
        if not auto_matching_check(app, sc_list):
            return False
    client.close()
    return True


def save_app_instance_db(app_id, app_instance_ids):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    client.app_db.app.insert_one({
        "app_id": app_id,
        "app_instance_ids": app_instance_ids
    })
    client.close()
    return True


def auto_matching_check(app, sc_list):
    sensor_oid_set = set()
    sensor_map = {}
    controller_map = {}
    for i in app["sensors"]:
        flag = False
        sensor_type = i["type"]
        for j in sc_list:
            s_type = j["type"]
            sensor_oid = j["_id"]
            if sensor_type.casefold() == s_type.casefold():
                if sensor_oid not in sensor_oid_set:
                    flag = True
                    sensor_oid_set.add(sensor_oid)
                    sensor_map[i["index"]] = sensor_oid
                    break
        if flag == False:
            return False, sensor_map, controller_map

    for i in app["controllers"]:
        flag = False
        controller_type = i["type"]
        for j in sc_list:
            c_type = j["type"]
            sensor_oid = j["_id"]
            if controller_type.casefold() == c_type.casefold():
                if sensor_oid not in sensor_oid_set:
                    flag = True
                    sensor_oid_set.add(sensor_oid)
                    controller_map[i["index"]] = sensor_oid
                    break
        if flag == False:
            return False, sensor_map, controller_map

    return True, sensor_map, controller_map

    for controller in app["controllers"]:
        controller
    pass


def insert_app_info(app_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_instance.count_documents(app_record) > 0:
        log.info(f'{app_record} already present')
        return False
    client.app_db.app.insert_one(app_record)
    client.close()
    return True


insert_app_info({
    "app_id": "y348y5348853945903834534",
    "app_name": "sample app",
    "description": "bla-bla",
    "scripts": True,
    "controller": True,
    "sensor": True,
    "model": True,
    "database": True,
    "sensors": [
        {
            "index": 0,
            "type": "TEMP"
        },
        {
            "index": 1,
            "type": "TEMP"
        },
        {
            "index": 2,
            "type": "TEMP"
        }

    ],
    "controllers": [
        {
            "index": 0,
            "type": "DISPLAY"
        },
        {
            "index": 1,
            "type": "DISPLAY"
        },
        {
            "index": 2,
            "type": "DISPLAY"
        }
    ],
    "models": [
        {
            "model_id": "asdah899028390"
        },
        {
            "model_id": "asdah899028391"
        },
        {
            "model_id": "asdah899028393"
        }
    ]
})