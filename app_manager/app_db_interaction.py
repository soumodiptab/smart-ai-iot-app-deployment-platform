import os
import json
from genericpath import isfile
from logging import Logger
import logging
from pathlib import Path
import uuid
from pymongo import MongoClient
from platform_logger import get_logger
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator

#from jsonschema import validate
import glob
log = get_logger('app_manager', 'localhost:9094')


def validate_app_and_insert(zip_file_loc):
    #control_schema = json_config_loader('config/control.json')
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)
        # log.info(extract_path)
        # get all sensors and controllers
    if(os.path.isfile(extract_path+'/app.json')):
        log.info(extract_path+'/app.json')
    app_config = json_config_loader(extract_path+'/app.json')
    app_schema = json_config_loader('config/app_schema.json')
    errors = validate_object(app_config, app_schema)
    if errors:
        for err in errors:
            log.error(err)
            return False
    app_record = app_config
    app_record['app_id'] = uuid.uuid4().hex
    if(app_config['script']):
        scripts_config = json_config_loader(
            extract_path+'/config/control.json')  # json_file
        scripts_schema = json_config_loader(
            'config/control_schema.json')  # json_schema
        errors = validate_object(scripts_config, scripts_schema)
        if not errors:
            if not os.path.isfile(os.path.join(extract_path, scripts_config['main'])):
                log.error(' Main file doesnt exit')
                return False
            for script in scripts_config['scripts']:
                path = extract_path+'/'+script['filename']
                if(os.path.isfile(path)):
                    log.info(path)
                else:
                    log.error(f'{path} does not exist')
                    return False
        else:
            for err in errors:
                log.error(err)
            return False
        app_record['scripts'] = scripts_config['scripts']

    if(app_config['controller']):
        controllers = json_config_loader(
            extract_path+'/config/controllers.json')
        controllers_schema = json_config_loader(
            'config/controllers_schema.json')
        errors = validate_object(controllers, controllers_schema)
        if not errors:
            client = MongoClient("mongodb://localhost:27017/")
            for controller in controllers['instances']:
                ctrl_type = controller['type']
                if client.sc_db.sc_type.count_documents({"type": ctrl_type,  "device": "CONTROLLER"}) > 0:
                    log.info("controllers found")
                else:
                    log.error(
                        f" Controller: {controller} not found in platform")
                    return False
            client.close()
        else:
            for err in errors:
                log.error(err)
            return False
        app_record['controllers'] = controllers['instances']

    if(app_config['model']):
        models = json_config_loader(extract_path+'/config/models.json')
        models_schema = json_config_loader('config/models_schema.json')
        errors = validate_object(models, models_schema)
        if not errors:
            client = MongoClient("mongodb://localhost:27017/")
            for model in models['instances']:
                model_id = model['model_id']
                if client.ai_data.model_info.count_documents({'modelId': model_id}) > 0:
                    log.info(f"Model present:{model_id}")
                else:
                    log.error(f"Models :{model_id} not present")
                    return False
            client.close()
        else:
            for err in errors:
                log.error(err)
            return False
        app_record['models'] = models['instances']

    if(app_config['sensor']):
        sensors = json_config_loader(extract_path+'/config/sensors.json')
        sensors_schema = json_config_loader('config/sensors_schema.json')
        errors = validate_object(sensors, sensors_schema)
        if not errors:
            client = MongoClient("mongodb://localhost:27017/")
            for sensor in sensors['instances']:
                sensors_type = sensor['type']
                if client.sc_db.sc_type.count_documents({"type": sensors_type, "device": "SENSOR"}) > 0:
                    log.info("sensors exist in platform")
                else:
                    log.error(f"sensor :{sensor} not present")
                    return False
            client.close()
        else:
            for err in errors:
                log.error(err)
            return False
        app_record['sensors'] = sensors['instances']
    if not insert_app_info(app_record):
        log.error(f'Failed to insert Application information:{app_record}')
    return True

# validate_app_and_insert(zip_file_loc)


def validate_app_instance(app_config):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    app = client.app_db.app.find({"app_id": app_config["app_id"]})[0]
    for instance in app_config["instances"]:
        sc_list = client.sc_db.sc_instance.find(
            {"geo_location": instance["geo_loc"]})
        if not auto_matching(app, sc_list):
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


def auto_matching(app, sc_list):
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


def insert_app_info(app_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.app_db.app.count_documents(app_record) > 0:
        log.info(f'{app_record} already present')
        return False
    client.app_db.app.insert_one(app_record)
    log.info(f'New app inserted:{app_record}')
    client.close()
    return True


# insert_app_info({
#     "app_id": "as48y534885394590383434",
#     "app_name": "sample app3",
#     "description": "bla 2342",
#     "scripts": True,
#     "controller": True,
#     "sensor": True,
#     "model": True,
#     "database": True,
#     "sensors": [
#         {
#             "index": 1,
#             "type": "PRES"
#         },
#         {
#             "index": 2,
#             "type": "PRES"
#         },
#         {
#             "index": 2,
#             "type": "TEMP"
#         }

#     ],
#     "controllers": [
#         {
#             "index": 0,
#             "type": "DISPLAY"
#         },
#         {
#             "index": 1,
#             "type": "DISPLAY"
#         }
#     ],
#     "models": [
#         {
#             "model_id": "asdah899028390"
#         },
#         {
#             "model_id": "asdah899028393"
#         }
#     ]
# })
