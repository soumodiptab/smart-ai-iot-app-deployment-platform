from uuid import uuid4
from utils import send_message
from app_db_interaction import auto_matching_check, save_app_instance_db


def process_application(end_user_config):
    app_id = end_user_config["app_id"]
    application_instances = end_user_config["instances"]
    app_instance_ids = []
    for app_instance in application_instances:
        app_instance_id = uuid4().hex
        scheduler_config = {
            "message_type": "SCHED",
            "app_id": app_id,
            "app_instance_id": app_instance_id,
            "start_time": end_user_config["start_time"],
            "end_time": end_user_config["end_time"],
            "periodicity": end_user_config["periodicity"],
            "periodicity_unit": end_user_config["periodicity_unit"]
        }
        send_message('scheduler', scheduler_config)
    save_app_instance_db(app_id, app_instance_ids)
    pass
