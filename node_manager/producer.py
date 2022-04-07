from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["13.71.109.62:9092"],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


req = {"message_type": "SCHED_APP", "app_id": "40d0cd6cef354f7eb28804c496f3931d", "isModel": False, "app_instance_id": "0aee800db5e245bdbbd9afc1c1a215ff", "start_time": "13:53", "end_time": "05:35", "periodicity": "1", "burst_time": "1", "periodicity_unit": "Mins"}
deploy_producer.send("scheduler", req)
time.sleep(2)


