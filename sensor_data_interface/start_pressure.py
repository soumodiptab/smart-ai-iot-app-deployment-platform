# inputs : ip | port | temp range
from sensor import PRESSURE
from kafka import KafkaConsumer
import sys
from utils import json_config_loader
import json
KAFKA_SERVERS = json_config_loader(
    'config/kafka.json')["bootstrap_servers"]
if len(sys.argv) <= 3 and len(sys.argv) >= 4:
    print('Invalid input')
    exit(0)
IP = sys.argv[1]
PORT = sys.argv[2]
sensor_config = json_config_loader('config/sc_config.json')
if len(sys.argv) == 4:
    pressure_range = int(sys.argv[3])
print("-----------------------------------------------------------------------------------------")
print("{}:{} PRESSURE".format(IP, PORT))
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
    pressure_sensor = PRESSURE(IP, PORT)
    pressure_sensor.set_range(pressure_range)
    pressure_sensor.start()
except:
    print()
    print("-----------------------------------------------------------------------------------------")
    print('Shutting down...')
    print("-----------------------------------------------------------------------------------------")
