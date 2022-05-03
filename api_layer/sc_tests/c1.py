from itsdangerous import base64_decode
from kafka import KafkaConsumer
import json
import hashlib
import base64
import re


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


ip_port = "127.0.0.1_8080"
consumer = KafkaConsumer(ip_port, group_id=ip_port,
                         bootstrap_servers=['localhost:9094'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))


if __name__ == '__main__':
    print('::: <Controller INIT> :::')
    counter = 0
    for message in consumer:
        print(message.value)
        image_string = message.value["data"].encode('utf-8')
        image = base64.b64decode(image_string)
        print(image)
        print('Writing to img...')
        decodeit = open(f'img{counter}.png', 'wb')
        counter = counter+1
        decodeit.write(image)
        decodeit.close()
