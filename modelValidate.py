import json
from pymongo import MongoClient
def model_validate():
    f=open('packaging_details/application/config/models.json')
    model_req=json.load(f)
    client=MongoClient()
    client = MongoClient("mongodb://localhost:27017/")
    for models in model_req['instances']:
        model_id=models['model_id']
        if client.ai_data.model_info.count_documents({'modelId':model_id}) == 0:
            print("Model doesn't exist")
        else:
            print("Model exists")

model_validate()
