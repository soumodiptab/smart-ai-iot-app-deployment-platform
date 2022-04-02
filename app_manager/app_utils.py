from email.mime import application
from uuid import uuid4
from utils import get_hash
from platform_logger import get_logger
from utils import send_message
from app_db_interaction import auto_matching, get_application, save_app_instance_db, get_ip_port
log = get_logger('app_manager', 'localhost:9094')


def save_file_service(file):
    pass


def process_application(end_user_config):
    app_id = end_user_config["app_id"]
    app_instance_id = uuid4().hex
    end_user = "dummy-user"
    status, sensor_map, controller_map = auto_matching(
        app_id, end_user_config["geo_loc"])
    sensor_topics = []
    controller_topics = []
    for key in sensor_map.keys():
        sensor_id = sensor_map[key]
        ip_port_map = get_ip_port(sensor_id)
        ip_port = ip_port_map["ip"]+":"+ip_port_map["port"]
        sensor_topics.append(get_hash(ip_port))
        log.info(f"Bound : {ip_port} to {app_instance_id} of {app_id}")
    for key in controller_map.keys():
        controller_id = controller_map[key]
        ip_port_map = get_ip_port(controller_id)
        ip_port = ip_port_map["ip"]+":"+ip_port_map["port"]
        controller_topics.append(get_hash(ip_port))
        log.info(f"Bound : {ip_port} to {app_instance_id} of {app_id}")
    application = get_application(app_id)
    save_app_instance_db({
        "app_id": app_id,
        "app_instance_id": app_instance_id,
        "end_user": end_user,
        "sensors": sensor_topics,
        "controllers": controller_topics,
        "models": application["models"]})
    scheduler_config = {
        "message_type": "SCHED_APP",
        "app_id": app_id,
        "app_instance_id": app_instance_id,
        "start_time": end_user_config["start_time"],
        "end_time": end_user_config["end_time"],
        "periodicity": end_user_config["periodicity"],
        "periodicity_unit": end_user_config["periodicity_unit"]
    }
    log.info(
        f"New app scheduled app_instance_id={app_instance_id}::: app_id={app_id}")
    send_message('scheduler', scheduler_config)
