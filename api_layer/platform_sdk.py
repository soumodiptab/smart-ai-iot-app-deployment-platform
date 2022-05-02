from utils import json_config_loader
from http import client
from io import BytesIO
from flask import request
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
import hashlib
import json
import requests
import base64
import threading
import logging
import json
import time
from kafka import KafkaProducer
LOGGER_TOPIC = 'logging'


class KafkaHandler(logging.Handler):
    def __init__(self, sys_name, host_port, topic):
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(
            bootstrap_servers=host_port, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic
        self.sys_name = sys_name

    def emit(self, record):
        if 'kafka.' in record.name:
            return
        try:
            self.formatter = logging.Formatter(
                '%(asctime)s ::: %(name)s ::: %(levelname)s ::: %(message)s')
            msg = self.format(record).strip()
            self.producer.send(self.topic, {
                'timestamp': record.asctime,
                'level': record.levelname,
                'sys_name': self.sys_name,
                'message': record.message})
            self.flush(timeout=1.0)
        except:
            logging.Handler.handleError(self, record)

    def flush(self, timeout=None):
        self.producer.flush(timeout=timeout)

    def close(self):
        try:
            if self.producer:
                self.producer.close()
            logging.Handler.close(self)
        finally:
            self.release()


def get_logger(sys_name, host_port, level=logging.DEBUG):
    logger = logging.getLogger(sys_name)
    logger.setLevel(level)
    kh = KafkaHandler(sys_name, host_port, LOGGER_TOPIC)
    logger.addHandler(kh)
    return logger


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


def json_config_loader(config_file_loc):
    fstream = open(config_file_loc, "r")
    data = json.loads(fstream.read())
    return data


KAFKA_SERVERS = json_config_loader(
    'config/kafka.json')['bootstrap_servers']
MONGO_IP_PORT = json_config_loader('config/db.json')["DATABASE_URI"]
MONGO_DB_URL = f"{MONGO_IP_PORT}"
app_instance_connection = MongoClient(MONGO_IP_PORT)


def get_mongo_db_uri():
    """ Fetch mongo db uri from platform

    Returns:
        _type_: _description_
    """
    return MONGO_DB_URL


def get_mongo_db_database():
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    app_instance_db = app_instance_connection[app_instance_id]
    return app_instance_db


def send_email_notification(email, subject, body):
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    producer = KafkaProducer(bootstrap_servers=kafka_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('email_notifier',
                  {
                      "command": "SEND",
                      "app_instance_id": app_instance_id,
                      "email_id": email,
                      "body": body,
                      "subject": subject
                  })


def get_sensor_image(sensor_index):
    """Return image

    Args:
        sensor_index (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    log = get_logger(app_instance_id, kafka_servers)
    client = MongoClient(MONGO_DB_URL)
    app_instance = client.app_db.instance.find_one(
        {"app_instance_id": app_instance_id})
    try:
        sensor_topic = app_instance["sensors"][sensor_index]
    except:
        log.error(f'Out of bounds sensor {sensor_index}')
        raise Exception('::: SENSOR EXCEPTION :::')
    client.close()

    try:
        consumer = KafkaConsumer(
            sensor_topic, group_id=app_instance_id, bootstrap_servers=kafka_servers, value_deserializer=lambda x: json.loads(x.decode('utf-8')), auto_offset_reset='latest')
        for message in consumer:
            image_string = message.value["data"].encode('utf-8')
            image = base64.b64decode(image_string)
            consumer.close()
            return image
    except:
        log.error(
            f'Error getting data from ::: {sensor_topic} for instance:{app_instance_id}')
        raise Exception('::: SENSOR EXCEPTION :::')


def get_stream_image(sensor_index, number_of_images):
    """Return image stream

    Args:
        sensor_index (_type_): _description_

    Raises:
        Exception: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    #log = get_logger(app_instance_id, kafka_servers)
    # client = MongoClient(MONGO_DB_URL)
    # app_instance = client.app_db.instance.find_one(
    #     {"app_instance_id": app_instance_id})
    # try:
    #     sensor_topic = app_instance["sensors"][sensor_index]
    # except:
    #     log.error(f'Out of bounds sensor {sensor_index}')
    #     raise Exception('::: SENSOR EXCEPTION :::')
    # client.close()
    # --------change--------
    counter = number_of_images
    app_instance_id = "234324sdfsfsd2"
    sensor_topic = "127.0.0.1_8080"
    images = []
    try:
        consumer = KafkaConsumer(
            sensor_topic, group_id=app_instance_id, bootstrap_servers=kafka_servers, value_deserializer=lambda x: json.loads(x.decode('utf-8')), auto_offset_reset='latest')
        for message in consumer:
            image_string = message.value["data"].encode('utf-8')
            image = base64.b64decode(image_string)
            images.append(image)
            counter = counter-1
            #stream = BytesIO(message.value)
            if counter <= 0:
                consumer.close()
                return images
    except:
        # log.error(
        #     f'Error getting data from ::: {sensor_topic} for instance:{app_instance_id}')
        raise Exception('::: SENSOR EXCEPTION :::')


def get_sensor_data(sensor_index):
    """Get Sensor data by providing index mapped in config file

    Args:
        sensor_index (_type_): index in sensor config file

    Raises:
        Exception: SENSOR EXCEPTION

    Returns:
        _type_: sensor data
    """

    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    log = get_logger(app_instance_id, kafka_servers)
    client = MongoClient(MONGO_DB_URL)
    app_instance = client.app_db.instance.find_one(
        {"app_instance_id": app_instance_id})
    try:
        sensor_topic = app_instance["sensors"][sensor_index]
    except:
        log.error(f'Out of bounds sensor {sensor_index}')
        raise Exception('::: SENSOR EXCEPTION :::')
    client.close()

    try:
        consumer = KafkaConsumer(sensor_topic, group_id=app_instance_id, bootstrap_servers=kafka_servers, auto_offset_reset="latest",
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for message in consumer:
            sensed_data = message.value['data']
            consumer.close()
            return sensed_data
    except:
        log.error(
            f'Error getting data from ::: {sensor_topic} for instance:{app_instance_id}')
        raise Exception('::: SENSOR EXCEPTION :::')


def send_controller_data(controller_index, *args):
    """ Send data to controller using index

    Args:
        controller_index (_type_): index of controller

    Raises:
        Exception: _description_
    """
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    log = get_logger(app_instance_id, kafka_servers)
    client = MongoClient(MONGO_DB_URL)
    app_instance = client.app_db.instance.find_one(
        {"app_instance_id": app_instance_id})
    try:
        controller_topic = app_instance["controllers"][controller_index]
    except:
        log.error(f'Out of bounds sensor {controller_index}')
        raise Exception('::: CONTROLLER EXCEPTION :::')
    client.close()
    try:
        producer = KafkaProducer(bootstrap_servers=kafka_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(controller_topic, {"data": args})
    except:
        log.error(
            f'Error sending data to ::: {controller_topic} for instance:{app_instance_id}')
        raise Exception('::: CONTROLLER EXCEPTION :::')


def get_prediction(model_index, json_obj):
    client = MongoClient(MONGO_DB_URL)
    # Todo feature for counting stats
    app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    model_id = json_config_loader(
        'config/models.json')["instances"][model_index]["model_id"]
    model = client.node_manager_db.app_deployment_metadata.find_one(
        {"_appId": model_id})
    ip_port = model["ip"]+":"+str(model["port"])
    client.close()
    prediction_api = f"http://{ip_port}/predict/{model_id}"
    json_out = requests.post(prediction_api, json=json_obj).json()
    return json_out


def get_prediction_using_image(model_index, image_obj):
    """ Use to get prediction from a model that uses image input

    Args: image object

    Returns:
        _type_: json object
    """
    # client = MongoClient(MONGO_DB_URL)
    # # Todo feature for counting stats
    # app_instance_id = json_config_loader('config/app.json')['app_instance_id']
    # model_id = json_config_loader(
    #     'config/models.json')["instances"][model_index]["model_id"]
    # model = client.node_manager_db.app_deployment_metadata.find_one(
    #     {"_appId": model_id})
    # ip_port = model["ip"]+":"+str(model["port"])
    # client.close()
    # ----------------change-------
    ip_port = "127.0.0.1:4901"
    model_id = "34sdf24234tyhtrhr2424"
    prediction_api = f"http://{ip_port}/predict/{model_id}"
    json_out = requests.post(prediction_api, files={'image': image_obj}).json()
    return json_out

# ----------------------------------------------------------------------------------------------------------


class HeartBeatClient(threading.Thread):
    def __init__(self, sleep_time=5):
        # system -> application | model
        # system = id for servers and system = container id for
        threading.Thread.__init__(self)
        self.ip = requests.get('http://api.ipify.org').text
        self.daemon = True
        self.topic = self.set_topic()
        self.heart_beat_topic = 'heartbeat_stream'
        self.sleep_time = sleep_time
        self.set_producer()
        self._stopevent = threading.Event()
        self.register_message = {
            "type": "server",
            "request": "register",
            "ip": self.ip,
            "topic": self.topic
        }

    def set_producer(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVERS, value_serializer=lambda v: v.encode('utf-8'))

    def set_topic(self):  # server
        return '{}-{}'.format("server", self.ip)

    def get_data(self):
        return '<*>'

    def register(self):
        self.producer.send(self.heart_beat_topic,
                           json.dumps(self.register_message))

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
            # register
            print('STARTING Heartbeat... from : {}'.format(self.ip))
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
    def __init__(self, service_id):  # Service name
        self.service_id = service_id
        super().__init__()
        self.register_message = {
            "type": "service",
            "request": "register",
            "ip": self.ip,
            "service_id": self.service_id,
            "topic": self.topic
        }

    def set_topic(self):
        return '{}-{}-{}'.format("service", self.ip, self.service_id)


class HeartBeatClientForApp(HeartBeatClient):
    def __init__(self, service_id):  # Service name
        self.service_id = service_id
        super().__init__()
        self.register_message = {
            "type": "app",
            "request": "register",
            "ip": self.ip,
            "service_id": self.service_id,
            "topic": self.topic
        }

    def set_topic(self):
        return '{}-{}-{}'.format("app", self.ip, self.service_id)


APP_INSTANCE_ID = json_config_loader('config/app.json')['app_instance_id']
# usage:
client = HeartBeatClientForService(APP_INSTANCE_ID)
client.start()
