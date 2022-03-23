from kafka import KafkaProducer
import json

producer = KafkaProducer(bootstrap_servers=[
    host_port], value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def send_heartbeat():
