from kafka import KafkaConsumer
import json
from platform_logger import get_logger
from requests import request
from utils import json_config_loader
import threading
KAFKA_SERVERS = json_config_loader('config/kafka.json')['bootstrap_servers']
log=get_logger('heartbeat',KAFKA_SERVERS)


class HeartBeatListener(threading.Thread):
    def __init__(self,listener_topic):
        threading.Thread.__init__(self)
        self.listener_topic = listener_topic
        self.daemon = True
        self.consumer = KafkaConsumer(self.listener_topic, group_id='heartbeat',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))
        self._stopevent = threading.Event()

    def run(self):
        for message in self.consumer:
            if self._stopevent.isSet():
                break
        self.consumer.close()

    def stop(self):
        self._stopevent.set()

global_directory={}




def start_listener_thread(topic_name):
    consumer = KafkaConsumer(topic_name, group_id='heartbeat',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))
    pass



def registration_process(message):
    topic=message["topic"]
    if message["type"]=="service":
        listener=HeartBeatListener(topic)
        listener.start()
        global_directory[topic]=listener

def unregistration_process(message):
    topic=message["topic"]
    if message["type"]=="service":
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
            if heartbeat_message["request"]=="register":
                registration_process(heartbeat_message)
            elif heartbeat_message["request"]=="unregister":
                unregistration_process(heartbeat_message)
            else:
                log.error('Unauthorized message type sent')
        except:
            print('Error processing  heartbeat message')
            log.error(f'Error processing message: {heartbeat_message}')

heartbeat_processor()