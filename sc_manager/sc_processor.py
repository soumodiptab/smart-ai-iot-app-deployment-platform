import logging
from kafka import KafkaConsumer
import json
from sc_db_interaction import app_sc_type_map, app_sc_instance_map
log = logging.getLogger('demo-logger')
sc_consumer = KafkaConsumer(
    "sc_manager",
    group_id='g1',
    bootstrap_servers=['localhost:9094'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in sc_consumer:
    message_type = msg.value["message_type"]
    log.info("New message recieved:{message_type}")
    log.info(msg.value)
    if message_type == "APP_SC_TYPE_MAP":
        app_sc_type_map(msg.value)
    if message_type == "APP_SC_INSTANCE_MAP":
        app_sc_instance_map(msg.value)
    else:
        log.info("Un-registered message")
