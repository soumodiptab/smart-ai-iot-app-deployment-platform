from kafka import KafkaProducer
import json
from faker import Faker
fake = Faker()
producer = KafkaProducer(bootstrap_servers=[
                         "localhost:9094"], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
message = {
    "message_type": "APP_SC_TYPE_MAP",
    "app_id": fake.uuid4(),
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
    ]
}
producer.send("sc_manager", message)
