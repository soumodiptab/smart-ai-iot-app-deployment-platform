from kafka import KafkaConsumer
import json
from utils import json_config_loader
KAFKA_SERVERS = json_config_loader('config/kafka.json')['bootstrap_servers']


def start_listener_thread(topic_name):
    consumer = KafkaConsumer(topic_name, group_id='heartbeat',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))

    pass


def heartbeat_processor():
    consumer = KafkaConsumer('heartbeat_stream', group_id='g',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))
    for message in consumer:
        # create a hearbeat watcher thread that waits for
        heartbeat_message = message.value
        heartbeat_stat = heartbeat_message.split("-")
        if heartbeat_stat[0] == "server":

            pass
        elif heartbeat_stat[0] == "service":
            pass
        elif heartbeat_stat[0] == "application":
            pass
        else:
            pass
