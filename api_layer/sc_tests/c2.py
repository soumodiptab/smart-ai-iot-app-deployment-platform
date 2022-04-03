from kafka import KafkaConsumer
import json

import hashlib


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


ip_port = "127.0.0.1:9061"
topic_name = '0d73e4fa9443abc370efa53afcefbdbc'
consumer = KafkaConsumer(topic_name, group_id="testing",
                         bootstrap_servers=['localhost:9094'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
if __name__ == '__main__':
    print('::: <Controller INIT> :::')
    for message in consumer:
        data = message.value["data"]
        print(f":::{data}:::")
