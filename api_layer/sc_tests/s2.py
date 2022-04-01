from random import randint
from kafka import KafkaProducer
import json
import time
ip_port = "127.0.0.1:9052"

producer = KafkaProducer(bootstrap_servers=[
                         'localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
if __name__ == '__main__':
    while True:
        data = randint(1, 200)
        message = {"data": data}
        print(f":::{data}:::")
        producer.send(ip_port, message)
        time.sleep(1)
