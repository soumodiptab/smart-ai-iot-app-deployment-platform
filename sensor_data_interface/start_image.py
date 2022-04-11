# inputs : ip | port | temp range
from sensor import IMAGE
from kafka import KafkaConsumer
import sys
from utils import json_config_loader
import json
import os
KAFKA_SERVERS = json_config_loader(
    'config/kafka.json')["bootstrap_servers"]
if len(sys.argv) <= 3 and len(sys.argv) >= 4:
    print('Invalid input')
    exit(0)
IP = sys.argv[1]
PORT = sys.argv[2]
sensor_config = json_config_loader('config/sc_config.json')
data_source = sensor_config["IMAGE"]["data_source"]

if len(sys.argv) == 4:
    data_source = sys.argv[3]
    if not os.path.exists(data_source) and not os.path.isdir(data_source):
        print('Error opening directory')
        exit(0)

print("-----------------------------------------------------------------------------------------")
print("{}:{} IMAGE".format(IP, PORT))
print()
print("-----------------------------------------------------------------------------------------")
listener_topic = "START_{}_{}".format(IP, PORT)
try:
    consumer = KafkaConsumer(
        listener_topic,
        group_id='simulator',
        bootstrap_servers=KAFKA_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    # Sensor start
    for message in consumer:
        break
    consumer.close()
    image_sensor = IMAGE(IP, PORT)
    image_sensor.set_data_source(data_source)
    image_sensor.start()
except:
    print()
    print("-----------------------------------------------------------------------------------------")
    print('Shutting down...')
    print("-----------------------------------------------------------------------------------------")
