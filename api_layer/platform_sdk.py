from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer, KafkaProducer
import hashlib
import json


def create_config_files(app_instance_id):
    pass


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()


def get_sensor_data(sensor_index):
    """Get Sensor data by providing index mapped in config file

    Args:
        sensor_index (_type_): index in sensor config file

    Raises:
        Exception: SENSOR EXCEPTION

    Returns:
        _type_: sensor data
    """
    sensor_map = json_config_loader('config/sensor_map.json')
    app = json_config_loader('config/app.json')
    app_instance_id = app['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    sensor_bus = sensor_map['mapping']
    topic_name = get_hash(sensor_bus[sensor_index])
    log = get_logger(app_instance_id, kafka_servers)
    try:
        consumer = KafkaConsumer(topic_name, group_id=app_instance_id, bootstrap_servers=kafka_servers,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for message in consumer:
            sensed_data = message.value['data']
            return sensed_data
    except:
        log.error(
            f'Error getting data from ::: {topic_name} for instance:{app_instance_id}')
        raise Exception('::: SENSOR EXCEPTION :::')

        # get info from sensor.json id -> type
        # sensor_type = json_config_loader(
        #     "config/sensors.json")["instances"]
        # # sensor type -> sensor instance
        # # generate app_id.jsonat the time of deployment
        # app_instance_id = json_config_loader("app_id.json")["app_id"]
        # MONGO_DB_URL = "mongodb://localhost:27017/"
        # client = MongoClient(MONGO_DB_URL)
        # client.sc_db.app_sc_bind.find({"app_instance_id": app_instance_id})
        # topic name - <ip-port>:<port>


def send_controller_data(controller_index, *args):
    """ Send data to controller using index

    Args:
        controller_index (_type_): index of controller

    Raises:
        Exception: _description_
    """
    app = json_config_loader('config/app.json')
    app_instance_id = app['app_instance_id']
    kafka_servers = json_config_loader(
        'config/kafka.json')['bootstrap_servers']
    ip_port = json_config_loader('config/host_file.json')
    controller_map = json_config_loader('config/controller_map.json')
    controller_bus = controller_map['mapping']
    topic_name = get_hash(controller_bus[controller_index])
    log = get_logger(app_instance_id, kafka_servers)
    try:
        producer = KafkaProducer(bootstrap_servers=kafka_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(topic_name, {"data": args})
    except:
        log.error(
            f'Error sending data to ::: {topic_name} for instance:{app_instance_id}')
        raise Exception('::: CONTROLLER EXCEPTION :::')
