from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["104.211.204.221:9092"],
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'))


req = {"message_type": "SCHED_APP", "app_id": "00f8fd2f9968428b85887ce42ee0b16f", "isModel": True, "app_instance_id": "00f8fd2f9968428b85887ce42ee0b16f",
       "start_time": "21:36", "end_time": "05:35", "periodicity": "5", "burst_time": "1", "periodicity_unit": "Hrs"}
deploy_producer.send("scheduler", req)
time.sleep(2)
