from kafka import KafkaConsumer
import json

sc_consumer = KafkaConsumer(
    "sc_route",
    group_id='g1',
    bootstrap_servers=['localhost:9094'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in sc_consumer:
    print(message)
    