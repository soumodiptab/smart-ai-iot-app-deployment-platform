
import json
from logging import Logger
import logging
from pathlib import Path
# from platform_logger import get_logger
from pymongo import MongoClient
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator
from platform_logger import get_logger
import glob
import uuid
import os
from jsonschema import validate, ValidationError, SchemaError
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
log = get_logger('ai_manager', KAFKA_SERVERS)
MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']


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
        data_sc_ai_model_schema = json_config_loader(
            extract_path + '/config.json')

        print(data_sc_ai_model_schema)

        # Validate the JSON schema
        if "name" in data_sc_ai_model_schema and "description" in data_sc_ai_model_schema\
                and "readme" in data_sc_ai_model_schema \
                and "preprocessing" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["preprocessing"] and "method_name" in data_sc_ai_model_schema["preprocessing"] and "input_params" in data_sc_ai_model_schema["preprocessing"] and "output_params" in data_sc_ai_model_schema["preprocessing"]\
                and "prediction" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["prediction"] and "model_type" in data_sc_ai_model_schema["prediction"] and "method_name" in data_sc_ai_model_schema["prediction"] and "input_params" in data_sc_ai_model_schema["prediction"] and "output_params" in data_sc_ai_model_schema["prediction"]\
                and "postprocessing" in data_sc_ai_model_schema and "name" in data_sc_ai_model_schema["postprocessing"] and "method_name" in data_sc_ai_model_schema["postprocessing"] and "input_params" in data_sc_ai_model_schema["postprocessing"] and "output_params" in data_sc_ai_model_schema["postprocessing"]\
                and "dependency" in data_sc_ai_model_schema:

            # Checking file exists or not

            readmeFile = data_sc_ai_model_schema["readme"]
            preprocessingFile = data_sc_ai_model_schema["preprocessing"]["name"]
            predictionFile = data_sc_ai_model_schema["prediction"]["name"]
            postprocessingFile = data_sc_ai_model_schema["postprocessing"]["name"]
            dependencyFile = data_sc_ai_model_schema["dependency"]

            # print(readmeFile + " " + preprocessingFile + " " + predictionFile + " " + postprocessingFile + " " + dependencyFile)

            print("ReadMe Loc:" + extract_path + "/" + readmeFile)

            readmeFileExists = os.path.exists(extract_path + "/" + readmeFile)
            preprocessingFileExists = os.path.exists(
                extract_path + "/" + preprocessingFile)
            predictionFileExists = os.path.exists(
                extract_path + "/" + predictionFile)
            postprocessingFileExists = os.path.exists(
                extract_path + "/" + postprocessingFile)
            dependencyFileExists = os.path.exists(
                extract_path + "/" + dependencyFile)

            print(readmeFileExists)

            if(readmeFileExists and preprocessingFileExists and predictionFileExists and postprocessingFileExists and dependencyFileExists):
                print(
                    "model, preprocessing, postprocessing, config, readme, requirements file present in ZIP. Verified!!")
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
    client = MongoClient(MONGO_DB_URL)
    db = client["ai_data"]
    my_collection = db["model_info"]
    config = json.load(open(path + "/config.json"))
    modelName = config["name"]
    data = {'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp,
            'port': port, 'runningStatus': False, 'config': config, 'isModel': True}
    my_collection.insert_one(data)
