from kafka import KafkaConsumer
from utils import json_config_loader
import json
import threading
from random import randint


class CONTROLLER(threading.Thread):
    def __init__(self, ip, port, sleep_time=0):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.topic = self.ip+"_"+self.port
        self.sleep_time = sleep_time
        self.set_consumer()
        self._stopevent = threading.Event()

    def set_consumer(self):
        self.consumer = KafkaConsumer(self.topic, group_id="simulator", bootstrap_servers=json_config_loader('config/kafka.json')['bootstrap_servers'],
                                      auto_offset_reset='earliest', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def do_action(self, message):
        data = message.value["data"]
        print("<{}:{}> : ::\t{}\t::".format(self.ip, self.port, data))

    def run(self):
        for message in self.consumer:
            self.do_action(message)
            if self._stopevent.isSet():
                break
        self.consumer.close()

    def stop(self):
        self._stopevent.set()


class DISPLAY(CONTROLLER):
    def do_action(self, message):
        data = message.value["data"]
        print("<{}:{}>DISPLAY : ::\t{}\t::".format(self.ip, self.port, data))


class BUZZER(CONTROLLER):
    def do_action(self, message):
        print("<{}:{}>BUZZER : ::\tBEEP\t::".format(self.ip, self.port))
        print('\a')


class FAN(CONTROLLER):
    def do_action(self, message):
        data = message.value["data"]
        print("<{}:{}>FAN : ::\tSPEED: {}\t::".format(self.ip, self.port, data))
        print('\a')


class AC(CONTROLLER):
    def do_action(self, message):
        data = message.value["data"]
        print("<{}:{}>AC : ::\tTEMP: {}\t::".format(self.ip, self.port, data))
        print('\a')
