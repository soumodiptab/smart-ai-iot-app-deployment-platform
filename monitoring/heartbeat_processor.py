from kafka import KafkaConsumer
import json
from platform_logger import get_logger
from requests import request
from utils import json_config_loader
import threading
from utils import send_message
HEARTBEAT_INTERVAL = json_config_loader('config/hearbeat.json')["INTERVAL"]
KAFKA_SERVERS = json_config_loader('config/kafka.json')['bootstrap_servers']
log = get_logger('heartbeat', KAFKA_SERVERS)


class HeartBeatListener(threading.Thread):
    def __init__(self, listener_topic, ip, service):
        threading.Thread.__init__(self)
        self.listener_topic = listener_topic
        self.daemon = True
        self.register = True
        self.consumer = KafkaConsumer(listener_topic, group_id='heartbeat', consumer_timeout_ms=HEARTBEAT_INTERVAL,
                                      bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))
        self._stopevent = threading.Event()
        self.service = service
        self.ip = ip
        self.service_agent="service_"

    def fault_tolerance(self):
        send_message(,
                     {
                         "COMMAND":"RESTART",
                         "IP":self.ip,

                     }
                     )

    def run(self):
        for message in self.consumer:
            if self._stopevent.isSet():
                break
        self.consumer.close()

    def stop(self):
        self._stopevent.set()


global_directory = {}


def registration_process(message):
    topic = message["topic"]
    if message["type"] == "service":
        listener = HeartBeatListener(topic)
        listener.start()
        global_directory[topic] = listener


def unregistration_process(message):
    topic = message["topic"]
    if message["type"] == "service":
        if topic not in global_directory:
            log.error(f' Missing topic for heartbeat: {topic}')
        else:
            global_directory.pop()


def heartbeat_processor():
    consumer = KafkaConsumer('heartbeat_stream', group_id='watcher',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        # create a hearbeat watcher that waits for heartbeatstream messages
        try:
            heartbeat_message = message.value
            if heartbeat_message["request"] == "register":
                registration_process(heartbeat_message)
            elif heartbeat_message["request"] == "unregister":
                unregistration_process(heartbeat_message)
            else:
                log.error('Unauthorized message type sent')
        except:
            print('Error processing  heartbeat message')
            log.error(f'Error processing message: {heartbeat_message}')


heartbeat_processor()
