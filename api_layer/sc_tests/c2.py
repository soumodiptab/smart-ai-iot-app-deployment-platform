from kafka import KafkaConsumer
import json

import hashlib


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


ip_port = "127.0.0.1_7001"
#topic_name = '0d73e4fa9443abc370efa53afcefbdbc'
topic_name = ip_port


def get_data():
    consumer = KafkaConsumer(topic_name, group_id="testing", auto_offset_reset="latest",
                             bootstrap_servers=["52.140.57.176:9092"], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        data = message.value["data"]
        print(f":::{data}:::")
        consumer.close()
        return data


if __name__ == '__main__':
    while True:
        get_data()
    print('::: <Controller INIT> :::')
