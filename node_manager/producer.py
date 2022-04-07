from kafka import KafkaProducer
import socket
import json
import time

deploy_producer = KafkaProducer(bootstrap_servers=["13.71.109.62:9092"],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


req = {"message_type": "SCHED_APP", "app_id": "02bff522cc2a4e348d7fef00902aac08", "isModel": True, "app_instance_id": "02bff522cc2a4e348d7fef00902aac08", "start_time": "19:16", "end_time": "05:35", "periodicity": "5", "burst_time": "1", "periodicity_unit": "Hrs"}
deploy_producer.send("scheduler", req)
time.sleep(2)


