from random import randint
from kafka import KafkaProducer
import json
import time
import hashlib
import base64
import pickle
ip_port = "127.0.0.1:9008"

producer = KafkaProducer(bootstrap_servers=[
                         'localhost:9094'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


if __name__ == '__main__':
    print(f"INIT: {get_hash(ip_port)}")
    while True:
        with open("download.png", "rb") as image_file:
            image = base64.b64encode(image_file.read())
            image_string = image.decode('utf-8')
            producer.send(get_hash(ip_port), {"data": image_string})
        time.sleep(3)
        print('Sending image')
