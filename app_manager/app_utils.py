from email.mime import application
from uuid import uuid4

from flask import jsonify
from utils import get_hash
from platform_logger import get_logger
from utils import send_message, json_config_loader
import requests
import time
from azure_blob import upload_blob, download_blob
from app_db_interaction import auto_matching, get_application, save_app_instance_db, get_ip_port, save_scheduling_info_db
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
log = get_logger('app_manager', KAFKA_SERVERS)


def save_file_service(file, fileName):
    upload_blob(file, fileName)


def process_application(end_user_config, username):
    app_id = end_user_config["app_id"]
    app_instance_id = uuid4().hex
    end_user = username
    status, sensor_map, controller_map = auto_matching(
        app_id, end_user_config["geo_loc"])
    sensor_topics = []
    controller_topics = []
    for key in sensor_map.keys():
        sensor_id = sensor_map[key]
        ip_port_map = get_ip_port(sensor_id)
        ip_port = ip_port_map["ip"]+"_"+ip_port_map["port"]
        sensor_topics.append(ip_port)
        log.info(f"Bound : {ip_port} to {app_instance_id} of {app_id}")
    for key in controller_map.keys():
        controller_id = controller_map[key]
        ip_port_map = get_ip_port(controller_id)
        ip_port = ip_port_map["ip"]+"_"+ip_port_map["port"]
        controller_topics.append(ip_port)
        log.info(f"Bound : {ip_port} to {app_instance_id} of {app_id}")
    application = get_application(app_id)
    save_app_instance_db({
        "app_id": app_id,
        "app_instance_id": app_instance_id,
        "end_user": end_user,
        "sensors": sensor_topics,
        "controllers": controller_topics,
        "models": application["models"]})
    # save_scheduling_info_db({
    #     "message_type": "SCHED_APP",
    #     "app_id": app_id,
    #     "isModel":false
    #     "app_instance_id": app_instance_id,
    #     "start_time": end_user_config["start_time"],
    #     "end_time": end_user_config["end_time"],
    #     "periodicity": end_user_config["periodicity"],
    #     "burst_time":end_user_config['burst_time'],
    #     "periodicity_unit": end_user_config["periodicity_unit"]
    # })
    scheduler_config = {
        "message_type": "SCHED_APP",
        "app_id": app_id,
        "isModel": False,
        "app_instance_id": app_instance_id,
        "start_time": end_user_config["start_time"],
        "end_time": end_user_config["end_time"],
        "periodicity": end_user_config["periodicity"],
        "burst_time": end_user_config['burst_time'],
        "periodicity_unit": end_user_config["periodicity_unit"]
    }
    # data = {"app_id": app_id, "app_instance_id": app_instance_id, "isModel": "false"}
    # requests.post(url = "http://127.0.0.1:5002/deployer/deploy/start", data = data)
    log.info(
        f"New app scheduled app_instance_id={app_instance_id}::: app_id={app_id}")
    send_message('scheduler', scheduler_config)
    time.sleep(1)
