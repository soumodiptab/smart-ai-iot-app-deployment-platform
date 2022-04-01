from kafka import KafkaConsumer
import json

ip_port = "127.0.0.1:9062"
consumer = KafkaConsumer(ip_port, group_id=ip_port,
                         bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
if __name__ == '__main__':
    print('::: <Controller INIT> :::')
    for message in consumer:
        data = message.val["data"]
        print(f":::{data}:::")
