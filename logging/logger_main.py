from kafka import KafkaConsumer
import json
consumer = KafkaConsumer('logging', group_id='g',
                         bootstrap_servers=["13.71.109.62:9092"], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
for message in consumer:
    print(message.value)
