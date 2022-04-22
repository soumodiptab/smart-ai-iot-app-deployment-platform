import os
import json
from pymongo import MongoClient
import docker
from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer
import requests
CURRENT_IP = requests.get('http://api.ipify.org').text
#CURRENT_IP = "218.185.248.66"
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
service_topic = "service"+"_"+CURRENT_IP
log = get_logger(service_topic, KAFKA_SERVERS)
MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
docker_client = docker.from_env()
INITIALIZER_DB = "initialiser_db"
COLLECTION = "services"
SLC = "running_services"
REPO_LOCATION = ".."


def show_containers():
    # displays all containers
    image_list = docker_client.images.list()
    container_list = docker_client.containers.list(True)
    pass


def get_stats(container_name):
    # need to decipher cpu / memory
    container = docker_client.containers.get(container_name)
    status = container.stats(decode=None, stream=False)
    return status


def is_container_exist(container_name):
    try:
        container = docker_client.containers.get(container_name)
        return True
    except:
        return False


def is_container_exited(container_name):
    try:
        container = docker_client.containers.get(container_name)
    except:
        return False
    if container.status == 'exited':
        return True
    return False


def start_service(service):
    client = MongoClient(MONGO_DB_URL)
    init_db = client[INITIALIZER_DB]
    services_col = init_db[COLLECTION]
    slc_col = init_db[SLC]
    try:
        service_info = services_col.find_one(
            {"service": service})
        if service_info["dockerised"] == "1":
            if is_container_exist(service):
                if not is_container_exited(service):
                    log.info(f'Service is already alive: {service}')
                else:
                    os.system(f'docker restart {service}')
                    log.info(f'service: {service} has been restarted')
            else:  # start a fresh service
                launch_directory = service_info["directory"]
                try:
                    service_image = docker_client.images.get(service)
                except:
                    image_path = os.path.join(
                        REPO_LOCATION, launch_directory)
                    docker_client.images.build(path=image_path, tag=service)
                data = {
                    "port_status": "0",
                    "ip": CURRENT_IP
                }
                port_req = False
                try:
                    PORT = service_info["port"]
                    data["port_status"] = "1"
                    data["port"] = PORT
                    port_req = True
                except:
                    log.info('No port registered for service')
                if port_req:
                    os.system(
                        f'docker run -d -p {PORT}:{PORT} --name {service} {service}')
                else:
                    os.system(
                        f'docker run -d --name {service} {service}')
                slc_col.update_one({"service": service}, {
                    "$set": data}, upsert=True)
                log.info(f'service: {service} has started')
                # root = os.getcwd()
        else:
            log.error('Does not support non-dockerized module')
            pass

    except:
        log.error('Error processing request')
    finally:
        client.close()


def stop_service(service):
    client = MongoClient(MONGO_DB_URL)
    init_db = client[INITIALIZER_DB]
    services_col = init_db[COLLECTION]
    slc_col = init_db[SLC]
    try:
        service_info = client.initializer_db.services.find_one(
            {"service": service})
        if service_info["dockerized"] == "1":
            if is_container_exist(service):
                if is_container_exited(service):
                    log.info(f'Service is already exited: {service}')
                else:  # unregister from heartbeat
                    os.system(f'docker stop {service}')
                    slc_col.delete_one({"service": service})
            else:
                log.error(f'{service} Container does not exist to stop')
        else:
            log.error('Does not support non-dockerized module')
            pass
    except:
        log.error('Error processing request')
    finally:
        client.close()


def listener():
    consumer = KafkaConsumer(service_topic, group_id='service_agent',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    log.info('Starting service agent consumer')
    for message in consumer:
        msg = message.value
        try:
            if msg["command"] == "START":
                start_service(msg["service"])
            elif msg["command"] == "STOP":
                stop_service(msg["service"])
            else:
                log.error(f'Invalid command issued: {msg}')
        except:
            log.error(' Invalid message scheme')


def decorator():
    self_ip = CURRENT_IP
    print('-------------------------------------------------------------------------')
    print(f' SERVICE AGENT: {self_ip}')
    print('-------------------------------------------------------------------------')


if __name__ == '__main__':
    decorator()
    listener()
