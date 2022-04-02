from pymongo import MongoClient
from utils import json_config_loader
from platform_logger import get_logger

log = get_logger('ai_manager', json_config_loader(
    'config/kafka.json')['bootstrap_servers'])


def insert_model_info(model_record):
    MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
    client = MongoClient(MONGO_DB_URL)
    if client.ai_data.model_info.count_documents(model_record) > 0:
        log.info(f'{model_record} already present')
        return False
    client.ai_data.model_info.insert_one(model_record)
    client.close()
    print('new model inserted')
    return True


# insert_model_info({
#     "deployedAddress": "http://127.0.0.1:6000",
#     "modelId": "2a30824424224c689b72e82e6690e74c",
#     "modelName": "model2",
#     "deployedIp": "http://127.0.0.1",
#     "port": 5000,
#     "config": {
#         "type": "Face Recog System",
#         "description": "adasdasda adasda ",
#         "readme": "readme.md",
#         "preprocessing": {
#             "name": "preprocess.py",
#             "method_name": "preprocess",
#             "input_params": [{
#                 "perc": "float",
#                 "temp_max": "float"
#             }],
#             "output_params": [{
#                 "perc": "float",
#                 "temp_max": "float"
#             }]
#         },
#         "prediction": {
#             "name": "model.pkl",
#             "method_name": "predict",
#             "input_params": [{
#                 "perc": "float",
#                 "temp_max": "float"
#             }],
#             "output_params": [{
#                 "type": "int"
#             }]
#         },
#         "dependency": "requirements.txt"
#     }
# })
