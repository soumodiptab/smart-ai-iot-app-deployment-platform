from genericpath import isfile
from logging import Logger
import logging
from pathlib import Path
from pymongo import MongoClient
from sympy import false, true
from utils import json_config_loader, get_file_name, validate_object
from zipfile import ZipFile
from jsonschema import Draft7Validator
#from jsonschema import validate
import glob
log = logging.getLogger('demo-logger')
import json
import os

#zip_file_loc="/home/sourav/IIITH/app.zip"
def validate_app_and_insert(zip_file_loc):
    #control_schema = json_config_loader('config/control.json')
    with ZipFile(zip_file_loc, 'r') as zip:
        log.info(f' Extracting Zip file :{zip_file_loc}')
        extract_path = zip_file_loc[:-4]
        zip.extractall(extract_path)
        #print(extract_path)
        # get all sensors and controllers

        f=open(extract_path+'/app.json')
        data = json.load(f)
        if(data['scripts']):
            control1=json_config_loader(extract_path+'/config/control.json')#json_file
            f1=open(extract_path+'/config/control.json')
            data1=json.load(f1)
            control = json_config_loader('config/control_schema.json')#json_schema
            errors = validate_object(control1, control)
            if not errors:
                for script in data1['scripts']:
                    path=extract_path+'/'+script['filename']
                    print(path)
                    if(os.path.isfile(path)):
                        print(isfile)
                    else:
                        print(1)
                    


        if(data['controllers']):
            control1=json_config_loader(extract_path+'/config/controllers.json')
            control = json_config_loader('config/controllers_schema.json')
            errors = validate_object(control1, control)
            if not errors:
                f=open(extract_path+'/config/models.json')
                control_req=json.load(f)
                client=MongoClient()
                client = MongoClient("mongodb://localhost:27017/")
                for controllers in control_req['instances']:
                    ctrl_type=controllers['type']
                    if client.sc_db.sc_type.count_documents({'type':ctrl_type}) == 0:
                        return true
                    else:
                        return false
                client.close()

        if(data['models']):
            control1=json_config_loader(extract_path+'/config/models.json')
            control = json_config_loader('config/models_schema.json')
            errors = validate_object(control1, control)
            if not errors:
                f=open(extract_path+'/config/models.json')
                model_req=json.load(f)
                client=MongoClient()
                client = MongoClient("mongodb://localhost:27017/")
                for models in model_req['instances']:
                    model_id=models['model_id']
                    if client.sc_db.sc_type.count_documents({'modelId':model_id}) == 0:
                        print("Model doesn't exist")
                    else:
                        print("Model exists")
                client.close()


        if(data['sensors']):
            control1=json_config_loader(extract_path+'/config/sensors.json')
            control = json_config_loader('config/sensors_schema.json')
            errors = validate_object(control1, control)
            if not errors:
                f=open(extract_path+'/config/sensors.json')
                sensors_req=json.load(f)
                client=MongoClient()
                client = MongoClient("mongodb://localhost:27017/")
                for sensors in sensors_req['instances']:
                    sensors_type=sensors['type']
                    if client.sc_db.sc_type.count_documents({'type':sensors_type}) == 0:
                        return true
                    else:
                        return false
                client.close()
            

#validate_app_and_insert(zip_file_loc)