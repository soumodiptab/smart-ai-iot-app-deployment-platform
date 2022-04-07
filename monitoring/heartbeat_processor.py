from kafka import KafkaConsumer
import json


def heartbeat_processor():
    consumer = KafkaConsumer('heartbeat_stream', group_id='g',
                             bootstrap_servers=['localhost:9094'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        print(message.value)
