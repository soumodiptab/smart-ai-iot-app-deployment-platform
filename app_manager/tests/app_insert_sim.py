from pymongo import MongoClient


def insert_app_info(app_record):
    MONGO_DB_URL = "mongodb://localhost:27017/"
    client = MongoClient(MONGO_DB_URL)
    if client.app_db.app.count_documents(app_record) > 0:
        print(f'{app_record} already present')
        return False
    client.app_db.app.insert_one(app_record)
    client.close()
    return True


insert_app_info({
    "app_id": "y348y5348853945903834534",
    "app_name": "sample app",
    "description": "bla-bla",
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
