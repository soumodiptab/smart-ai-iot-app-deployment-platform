from random import randint
from faker import Faker
from kafka import KafkaProducer
import json
import time
producer = KafkaProducer(bootstrap_servers=[
                         '172.24.0.3:9094'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
fake = Faker()
if __name__ == '__main__':
    while True:
        message = {
            "email": fake.email(),
            "name": fake.name()
        }
        print(message)
        producer.send('new-route', message)
        time.sleep(1)
