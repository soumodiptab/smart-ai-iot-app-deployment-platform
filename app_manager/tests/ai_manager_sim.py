from pymongo import MongoClient


def insert_model_info(model_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.ai_data.model_info.count_documents(model_record) > 0:
        print(f'{model_record} already present')
        return False
    client.ai_data.model_info.insert_one(model_record)
    client.close()
    print('new model inserted')
    return True


insert_model_info({
    "deployedAddress": "http://127.0.0.1:6000",
    "modelId": "2a30824424224c689b72e82e6690e74c",
    "modelName": "model2",
    "deployedIp": "http://127.0.0.1",
    "port": 5000,
    "config": {
        "type": "Face Recog System",
        "description": "adasdasda adasda ",
        "readme": "readme.md",
        "preprocessing": {
            "name": "preprocess.py",
            "method_name": "preprocess",
            "input_params": [{
                "perc": "float",
                "temp_max": "float"
            }],
            "output_params": [{
                "perc": "float",
                "temp_max": "float"
            }]
        },
        "prediction": {
            "name": "model.pkl",
            "method_name": "predict",
            "input_params": [{
                "perc": "float",
                "temp_max": "float"
            }],
            "output_params": [{
                "type": "int"
            }]
        },
        "dependency": "requirements.txt"
    }
})
