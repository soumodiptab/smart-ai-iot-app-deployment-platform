from kafka import KafkaConsumer
import json
from platform_logger import get_logger
from requests import request
from utils import json_config_loader
import threading
from utils import send_message
HEARTBEAT_INTERVAL = json_config_loader('config/heartbeat.json')["INTERVAL"]
KAFKA_SERVERS = json_config_loader('config/kafka.json')['bootstrap_servers']
log = get_logger('heartbeat', KAFKA_SERVERS)


class HeartBeatListener(threading.Thread):
    def __init__(self, listener_topic, ip, type):
        threading.Thread.__init__(self)
        self.listener_topic = listener_topic
        self.daemon = True
        self.register = True
        self.consumer = KafkaConsumer(listener_topic, group_id='heartbeat', consumer_timeout_ms=HEARTBEAT_INTERVAL,
                                      bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: x.decode('utf-8'))
        self._stopevent = threading.Event()
        self.ip = ip
        self.type = type
        self.service = "service_agent"
        self.service_agent = "service_"+ip

    def fault_tolerance(self):
        pass

    def run(self):
        log.info(f'Heartbeat listening on: {self.service} at {self.ip}')
        for message in self.consumer:
            if self._stopevent.isSet():
                self.register = False
                break
        if self.register:
            log.info(f'Hearbeat not found: {self.service} at {self.ip}')
            self.fault_tolerance()
        self.consumer.close()

    def stop(self):
        self._stopevent.set()


class HeartBeatListenerForService(threading.Thread):
    def __init__(self, listener_topic, ip, type, service):
        threading.Thread.__init__(self)
        super().__init__(listener_topic, ip, type)
        self.service = service

    def fault_tolerance(self):
        send_message(self.service_agent,
                     {
                         "command": "START",
                         "service": self.service,
                     })


global_directory = {}


def registration_process(message):
    topic = message["topic"]
    if message["type"] == "server":
        listener = HeartBeatListener(topic, message["ip"], message["type"])
        global_directory[listener.service_agent] = listener
    else:
        listener = HeartBeatListenerForService(
            topic, message["ip"], message["type"], message["service_id"])
        listener.start()
        global_directory[listener.service] = listener


def unregistration_process(message):
    service_id = message["service_id"]
    if message["type"] == "service":
        if service_id not in global_directory:
            log.error(f' Missing service for heartbeat: {service_id}')
        else:
            listener_thread = global_directory.pop()
            listener_thread.stop()
            log.info(f'Heartbeat unregistered for service: {service_id}')
    else:
        log.error('Unregistration process not supported')
        pass


def heartbeat_processor():
    consumer = KafkaConsumer('heartbeat_stream', group_id='watcher', enable_auto_commit=True, auto_offset_reset='latest',
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


#heartbeat_processor()
threading.Thread(target=heartbeat_processor, args=()).start()
print('HeartBeat PROCESSOR STARTED....')
