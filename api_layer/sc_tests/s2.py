from random import randint
from kafka import KafkaProducer
import json
import time
import hashlib


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


ip_port = "127.0.0.1_7021"
producer = KafkaProducer(bootstrap_servers=[
                         '20.219.102.74:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
if __name__ == '__main__':
    while True:
        data = randint(1, 200)
        message = {"data": data}
        print(f":::{data}:::")
        producer.send(ip_port, message)
        time.sleep(1)
