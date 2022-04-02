from random import randint
from kafka import KafkaProducer
import json
import time
import hashlib
ip_port = "127.0.0.1:9051"

producer = KafkaProducer(bootstrap_servers=[
                         'localhost:9094'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


if __name__ == '__main__':
    print(f"INIT: {get_hash(ip_port)}")
    while True:
        data = randint(1, 200)
        message = {"data": data}
        print(f":::{data}:::")
        producer.send(get_hash(ip_port), message)
        time.sleep(1)
