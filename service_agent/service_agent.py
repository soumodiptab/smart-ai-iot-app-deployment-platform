from asyncio import tasks
import os
from flask import Flask, flash, redirect, render_template, session, request, jsonify, url_for
import json
from bson.json_util import dumps
from matplotlib import container
from pymongo import MongoClient
import shutil
import threading
import docker
import requests
from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer
import yaml
# os.chdir('../ai_manager')
# print(os.getcwd())
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
log = get_logger('sensor_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
docker_client = docker.from_env()
INITIALIZER_DB = "initializer_db"
COLLECTION = "services"
with open("./config.yml", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)


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


def pull_repository():
    pass


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
    try:
        service_info = client.initializer_db.services.find_one(
            {"service": service})
        if service_info["dockerized"] == "1":
            if is_container_exist(service):
                if not is_container_exited(service):
                    log.info(f'Service is already alive: {service}')
                else:
                    os.system(f'docker restart {service}')
            else:  # start a fresh service
                launch_directory = service_info["directory"]
                container = docker_client.containers.get(service)
                try:
                    service_image = docker_client.images.get(service)
                except docker.errors.ImageNotFoundError:
                    docker_client.images.build(
                        os.path.join(os.getenv('REPO_LOCATION'),
                                     launch_directory)
                    )
                    # root = os.getcwd()
        else:
            pass

    except:
        log.error('Error processing request')
    finally:
        client.close()


def stop_service(service):
    #
    pass


def listener():
    ip = requests.get('https://api.ipify.org/').text
    service_topic = "service"+"_"+ip
    consumer = KafkaConsumer(service_topic, group_id='service_agent',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        msg = message.value
        try:
            if msg["command"] == "START":
                start_service(msg)
            elif msg["command"] == "STOP":
                stop_service(msg)
            else:
                log.error(f'Invalid command issued: {msg}')
        except:
            log.error(' Invalid message scheme')


def decorator():
    self_ip = requests.get('https: // api.ipify.org/').text
    print('-------------------------------------------------------------------------')
    print(f' SERVICE AGENT: {self_ip}')
    print('-------------------------------------------------------------------------')


if __name__ == '__main__':
    decorator()
    threading.Thread(target=listener, args=()).start()
    app.run(host="0.0.0.0", port=6000, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
