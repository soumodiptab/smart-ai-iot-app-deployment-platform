from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["13.71.109.62:9092"],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


deploy_producer.send("deploy_127.0.0.1", "hello asshole")
time.sleep(2)


