
import json
from logging import Logger
import logging
from pathlib import Path
# from platform_logger import get_logger
from pymongo import MongoClient
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator
import glob
import uuid
import os
from jsonschema import validate, ValidationError, SchemaError

#log = get_logger('sensor_manager', 'localhost:9094')
log=logging.getLogger('demo-logger')
# client -> sc_db -> sc_type | sc_instance
# sc_db = client["sc_db"]
# sc_type = sc_db["sc_type"]
# sc_instance = sc_db["sc_instance"]

# json schema for config file
# validator = Draft7Validator(sensor_type_schema)

def validate_ai_type(zip_file_loc):
    # first extract zip
    with ZipFile(zip_file_loc, 'r') as zip:
        print(str(zip_file_loc))
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)

        # Removing the zip file after extraction
        os.remove(zip_file_loc)

        platform_ai_model_schema = json_config_loader('./ai_model_schema.json')
        data_sc_ai_model_schema = json_config_loader(extract_path + '/config.json')

        print(data_sc_ai_model_schema)

        # Validate the JSON schema
        if "name" in data_sc_ai_model_schema and "description" in data_sc_ai_model_schema\
        and "readme" in data_sc_ai_model_schema \
        and "preprocessing" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["preprocessing"] and "method_name" in data_sc_ai_model_schema["preprocessing"] and "input_params" in data_sc_ai_model_schema["preprocessing"] and "output_params" in data_sc_ai_model_schema["preprocessing"]\
        and "prediction" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["prediction"] and "model_type" in data_sc_ai_model_schema["prediction"] and "method_name" in data_sc_ai_model_schema["prediction"] and "input_params" in data_sc_ai_model_schema["prediction"] and "output_params" in data_sc_ai_model_schema["prediction"]\
        and "postprocessing" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["postprocessing"] and "method_name" in data_sc_ai_model_schema["postprocessing"] and "input_params" in data_sc_ai_model_schema["postprocessing"] and "output_params" in data_sc_ai_model_schema["postprocessing"]\
        and "dependency" in data_sc_ai_model_schema :

            # Checking file exists or not
            
            readmeFile = data_sc_ai_model_schema["readme"]
            preprocessingFile = data_sc_ai_model_schema["preprocessing"]["name"]
            predictionFile = data_sc_ai_model_schema["prediction"]["name"]
            postprocessingFile = data_sc_ai_model_schema["postprocessing"]["name"]
            dependencyFile = data_sc_ai_model_schema["dependency"]

            # print(readmeFile + " " + preprocessingFile + " " + predictionFile + " " + postprocessingFile + " " + dependencyFile)
            
            print("ReadMe Loc:" + extract_path + "/" + readmeFile)

            readmeFileExists = os.path.exists(extract_path + "/" + readmeFile)
            preprocessingFileExists = os.path.exists(extract_path + "/" + preprocessingFile)
            predictionFileExists = os.path.exists(extract_path + "/" + predictionFile)
            postprocessingFileExists = os.path.exists(extract_path + "/" + postprocessingFile)
            dependencyFileExists = os.path.exists(extract_path + "/" + dependencyFile)

            print(readmeFileExists)
            
            if(readmeFileExists and preprocessingFileExists and predictionFileExists and postprocessingFileExists and dependencyFileExists):
                print("model, preprocessing, postprocessing, config, readme, requirements file present in ZIP. Verified!!")
            else:
                print("Some files are not present in ZIP")
                return False
        else:
            print("There is an error with the schema")
            return False
        
        return True

        # try:
        #     validate(platform_ai_model_schema, data_sc_ai_model_schema)
        #     print("JSON schema is valid!!")
        # except SchemaError as e:
        #     print("There is an error with the schema")
        #     return False
        
        # except ValidationError as e:
        #     print(e)
            
        #     print("---------")
        #     print(e.absolute_path)
        
        #     print("---------")
        #     print(e.absolute_schema_path)
        #     return False

        # try:
        #     readmeFile = data_sc_ai_model_schema["readme"]
        #     preprocessingFile = data_sc_ai_model_schema["preprocessing"]["name"]
        #     predictionFile = data_sc_ai_model_schema["prediction"]["name"]
        #     postprocessingFile = data_sc_ai_model_schema["postprocessing"]["name"]
        #     dependencyFile = data_sc_ai_model_schema["dependency"]

        #     # print(readmeFile + " " + preprocessingFile + " " + predictionFile + " " + postprocessingFile + " " + dependencyFile)
            
        #     readmeFileExists = os.path.exists(extract_path + readmeFile)
        #     preprocessingFileExists = os.path.exists(extract_path + preprocessingFile)
        #     predictionFileExists = os.path.exists(extract_path + predictionFile)
        #     postprocessingFileExists = os.path.exists(extract_path + postprocessingFile)
        #     dependencyFileExists = os.path.exists(extract_path + dependencyFile)

        #     if(readmeFileExists and preprocessingFileExists and predictionFileExists and postprocessingFileExists and dependencyFileExists):
        #         print("model, preprocessing, postprocessing, config, readme, requirements file present in ZIP. Verified!!")
        # except:
        #     print("!! Some files are not present in the zip !!")
        #     return False

        # return True

def insert_ai_model_info(modelId, path):
    deployedIp = ""
    port = ""
    # client = MongoClient('mongodb://localhost:27017/')
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    db = client["ai_data"]
    my_collection = db["model_info"]
    config = json.load(open(path + "/config.json"))
    modelName = config["name"]
    data = {'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp, 'port': port, 'runningStatus': False, 'config': config, 'isModelAI': True}
    my_collection.insert_one(data)

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
        for sensor_file in sensor_list:
            sensor = json_config_loader(sensor_file)
            errors = validate_object(sensor, sc_instance_schema)
            for error in errors:
                log.error(error)
                return False
            sensor_type = sensor["type"]
            if not check_sc_type("SENSOR", sensor_type):
                return False
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
            controller["device"] = "CONTROLLER"
            sc_list.append(controller)
            # if not insert_sc_instance_record(controller):
            #     return False
        for sc in sc_list:
            if not insert_sc_instance_record(sc):
                return False
            log.info(f"New device registered: {sc}")
    return True


def insert_sc_type_record(sc_type_record):
    # client = MongoClient('mongodb://localhost:27017/')
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_type.count_documents(sc_type_record):
        log.info(f'{sc_type_record} already present')
        return True
    client.sc_db.sc_type.insert_one(sc_type_record)
    client.close()
    return True


def insert_sc_instance_record(sc_instance_record):
    # client = MongoClient('mongodb://localhost:27017/')
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    if client.sc_db.sc_instance.count_documents(sc_instance_record) > 0:
        log.info(f'{sc_instance_record} already present')
        return False
    client.sc_db.sc_instance.insert_one(sc_instance_record)
    client.close()
    return True


def app_sc_type_map(message):
    # client = MongoClient('mongodb://localhost:27017/')
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    application_uuid = message["app_id"]
    sensors = message["sensors"]
    controllers = message["controllers"]
    for sensor in sensors:
        sensor
    client.close()
    pass


def check_sc_type(device, sc_type):
    # client = MongoClient('mongodb://localhost:27017/')
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    if not client.sc_db.sc_type.count_documents({"device": device, "type": sc_type}) > 0:
        log.info(f'Device: {device} Type:{sc_type} not present in Platform')
        return False
    client.close()
    return True


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
