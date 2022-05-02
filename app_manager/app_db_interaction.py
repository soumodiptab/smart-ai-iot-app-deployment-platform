from asyncio.log import logger
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
log = get_logger('ai_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
MONGO_DB_URL = json_config_loader('config/db.json')["DATABASE_URI"]
#log = logging.getLogger('demo-logger')


def validate_app_and_insert(app_id, zip_file_loc):
    #control_schema = json_config_loader('config/control.json')
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        print(extract_path)
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
    app_record['app_id'] = app_id
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
            client = MongoClient(MONGO_DB_URL)
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
            client = MongoClient(MONGO_DB_URL)
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
            client = MongoClient(MONGO_DB_URL)
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
    return True


def save_app_instance_db(app_instance_record):
    client = MongoClient(MONGO_DB_URL)
    client.app_db.instance.insert_one(app_instance_record)
    client.close()
    return True


def save_scheduling_info_db(scheduling_config):
    client = MongoClient(MONGO_DB_URL)
    client.scheduler.config.insert_one(scheduling_config)
    client.close()
    return True


def get_ip_port(sc_oid):
    try:

        client = MongoClient(MONGO_DB_URL)
        sc = client.sc_db.sc_instance.find_one({"_id": sc_oid})
        client.close()
        log.info(f"Sensor/controller query:{sc_oid}")
        return sc["ip_loc"]
    except:
        log.error(f"Error fetching application details{sc}")
        return None


def get_application(app_id):
    try:
        client = MongoClient(MONGO_DB_URL)
        application = client.app_db.app.find_one({"app_id": app_id})
        client.close()
        log.info(f"Application query:{app_id}")
        return application
    except:
        log.error(f"Error fetching application details{app_id}")
        return None


def auto_matching(app_id, geo_loc):
    sensor_oid_set = set()
    sensor_map = {}
    controller_map = {}
    client = MongoClient(MONGO_DB_URL)
    app = client.app_db.app.find_one({"app_id": app_id})
    sensor_list = client.sc_db.sc_instance.find(
        {"geo_location": geo_loc, "device": "SENSOR"})
    controller_list = client.sc_db.sc_instance.find(
        {"geo_location": geo_loc, "device": "CONTROLLER"}
    )
    if client.sc_db.sc_instance.count_documents({"geo_location": geo_loc}) == 0:
        log.error(f'No sensor controllers present in location {geo_loc}')
        return False, sensor_map, controller_map
    for i in app["sensors"]:
        flag = False
        sensor_type = i["type"]
        for j in sensor_list:
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
        for j in controller_list:
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
    client.close()
    return True, sensor_map, controller_map


def auto_matching_check(app_id, geo_loc):
    status, sensor_map, controller_map = auto_matching(app_id, geo_loc)
    return status


def insert_app_info(app_record):
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
