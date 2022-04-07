from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["13.71.109.62:9092"],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


req = {"message_type": "SCHED_APP", "app_id": "64af94339aba44e3a86504039cc85e26", "isModel": False, "app_instance_id": "63505624f61245d38ede707b3d805343", "start_time": "03:30", "end_time": "05:35", "periodicity": "1", "burst_time": "1", "periodicity_unit": "Hrs"}
deploy_producer.send("scheduler", req)
time.sleep(2)


