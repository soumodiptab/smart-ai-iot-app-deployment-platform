from kafka import KafkaConsumer
from kafka import KafkaProducer
from utils import json_config_loader
import json
import threading
from random import randint
import time
import base64
import glob
import random


class SENSOR(threading.Thread):
    def __init__(self, ip, port, sleep_time=5):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.topic = ip+"_"+port
        self.sleep_time = sleep_time
        self.set_producer()
        self._stopevent = threading.Event()

    def set_producer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=json_config_loader('config/kafka.json')['bootstrap_servers'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def get_data(self):
        pass

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
            while not self._stopevent.isSet():
                self.emit()
                self.timeout()
            self.producer.flush()
        finally:
            self.close()

    def stop(self):
        self._stopevent.set()


class TEMP(SENSOR):
    def set_range(self, temp_range):
        self.range = temp_range

    def get_data(self):
        data = randint(1, self.range)
        print("<{}:{}> TEMP : {}".format(self.ip, self.port, data))
        return {"data": data}


class PRESSURE(SENSOR):
    def set_range(self, temp_range):
        self.range = temp_range

    def get_data(self):
        data = randint(1, self.range)
        print("<{}:{}> PRESSURE : {}".format(self.ip, self.port, data))
        return {"data": data}


class IMAGE(SENSOR):
    def set_data_source(self, folder):
        self.img_folder = folder

    def get_data(self):
        image_list = glob.glob(f"{self.img_folder}/*.*")
        img_loc = random.choice(image_list)
        print('<{}:{}> IMAGE : sending: {}'.format(self.ip, self.port, img_loc))
        with open(img_loc, "rb") as image_file:
            image = base64.b64encode(image_file.read())
            image_string = image.decode('utf-8')
            return {"data": image_string}
