import time
from platform_logger import get_logger
from pymongo import MongoClient
from utils import json_config_loader, send_message
# temp_sensor = TEMP("127.0.0.1", "9061", {"street": "RANDOM", "city": "HYD"})
# type = 'IMAGE'
# geo_loc = str({"street": "RANDOM", "city": "HYD"})
# ip_port = '127.0.0.1:9008'
# latency = 13
# expression = 'sensor_interface.'+type + '('+'\"'+ip_port+'\"'+','+str(latency)+')'
# image_sensor = eval(expression)
# image_sensor.set_data_source('images/gun_detection')
# image_sensor.start()

import sys
IP = sys.argv[1]
PORT = sys.argv[2]
KAFKA_SERVERS = json_config_loader(
    'config/kafka.json')["bootstrap_servers"]
MONGODB_URL = json_config_loader('config/db.json')['DATABASE_URI']
#log = get_logger('sc_data_interface', KAFKA_SERVERS)
send_message("START_{}_{}".format(IP,PORT), {
    "message_type": "START_SC",
})
