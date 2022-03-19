from elasticsearch import Elasticsearch
import time
import json
from datetime import datetime
from kafka import KafkaConsumer
INDEX_NAME = "new-relic-log"


class Elastic:
    def __init__(self, host='localhost', port=9200, INDEX_NAME='new-relic-log'):
        self.host = host  # localhost
        self.port = port  # 9200
        self.es = None
        self.connect()
        self.INDEX_NAME = INDEX_NAME

    def connect(self):
        self.es = Elasticsearch([{'host': self.host, 'port': self.port}])
        if self.es.ping():
            print("ES connected successfully")
        else:
            print("Not connected")

    def create_index(self):
        if self.es.indices.exists(self.INDEX_NAME):
            print("deleting '%s' index..." % (self.INDEX_NAME))
            res = self.es.indices.delete(index=self.INDEX_NAME)
            print(" response: '%s'" % (res))
            request_body = {
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
            print("creating '%s' index..." % (self.INDEX_NAME))
            res = self.es.indices.create(
                index=self.INDEX_NAME, body=request_body, ignore=400)
            print(" response: '%s'" % (res))

    def push_to_index(self, message):
        try:
            response = self.es.index(
                index=INDEX_NAME,
                doc_type="log",
                body=message
            )
            print("Write response is :: {}\n\n".format(response))
        except Exception as e:
            print("Exception is :: {}".format(str(e)))


class LogConsumer:
    def __init__(self, topic, broker="localhost:9092", group="elk_consumer"):
        self.broker = broker
        self.group = group
        self.con = KafkaConsumer(
            {
                'bootstrap.servers': self.broker,
                'group.id': self.group,
                'auto.offset.reset': 'earliest'
            },
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.topic = topic
        self.con.subscribe([self.topic])

    def read_messages(self):
        try:
            msg = self.con.poll(0.1)
            if msg is None:
                return 0
            elif msg.error():
                return 0
            return msg
        except Exception as e:
            print("Exception during reading message :: {}".format(e))
            return 0


if __name__ == '__main__':
    es_obj = Elastic()
    es_obj.create_index()
    con = LogConsumer("logging",)
    while True:
        message = con.read_messages()
        if not message:
            continue
        time.sleep(0.4)
        es_obj.push_to_index(message)
