from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["52.172.25.250:9092"],
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'))


req = {"message_type": "SCHED_APP", "app_id": "af1aefd3878148e0922ef8c78f364b80", "isModel": True, "app_instance_id": "af1aefd3878148e0922ef8c78f364b80",
       "start_time": "17:53", "end_time": "05:35", "periodicity": "5", "burst_time": "1", "periodicity_unit": "Hrs"}
deploy_producer.send("scheduler", req)
time.sleep(2)
