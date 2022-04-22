from kafka import KafkaProducer
import json
import threading
import time
from utils import json_config_loader
KAFKA_SERVERS = json_config_loader('config/kafka.json')['bootstrap_servers']


class HeartBeatClient(threading.Thread):
    def __init__(self, ip, port, sleep_time=5):
        # system -> application | model
        # system = id for servers and system = container id for
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.daemon = True
        self.topic = self.set_topic()
        self.heart_beat_topic = 'heartbeat_stream'
        self.sleep_time = sleep_time
        self.set_producer()
        self._stopevent = threading.Event()
        self.register_message={
            "type":"server",
            "request":"register",
            "ip":self.ip,
            "port":self.port,
            "topic":self.topic
        }

    def set_producer(self):
        self.producer =KafkaProducer(bootstrap_servers=
        KAFKA_SERVERS, value_serializer=lambda v: v.encode('utf-8'))

    def set_topic(self):  # server
            return '{}-{}-{}'.format("server", self.ip, self.port)

    def get_data(self):
        return '<*>'

    def register(self):
        self.producer.send(self.heart_beat_topic,json.dumps(self.register_message))
    def emit(self):
        self.producer.send(self.topic, self.get_data())

    def flush(self, timeout=None):
        self.producer.flush(timeout=timeout)

    def timeout(self):
        time.sleep(self.sleep_time)

    def close(self):
        if self.producer:
            self.producer.close()

    def run(self):
        try:
            #register
            print('STARTING Heartbeat... from {} : {}'.format(self.ip,self.port))
            self.register()
            while not self._stopevent.isSet():
                self.emit()
                self.timeout()
            self.producer.flush()
        finally:
            self.close()

    def stop(self):
        self._stopevent.set()


class HeartBeatClientForService(HeartBeatClient):
    def __init__(self, ip, port, service_id):
        self.service_id = service_id
        super().__init__(ip, port)
        self.register_message={
            "type":"service",
            "request":"register",
            "ip":self.ip,
            "port":self.port,
            "service_id":self.service_id,
            "topic":self.topic
        }

    def set_topic(self):
        return '{}-{}-{}-{}'.format("service", self.ip, self.port, self.service_id)

    # usage:
client = HeartBeatClientForService('127.0.0.1', '6500', 'ai_manager')
client.start()
