from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('new-route',
                         bootstrap_servers=['localhost:9094'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
for message in consumer:
    msg = message.value
    print(msg)
