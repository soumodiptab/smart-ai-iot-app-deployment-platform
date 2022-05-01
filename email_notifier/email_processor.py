import os
import json
#from pymongo import MongoClient
from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer
import requests
import yagmail
from heartbeat_client import HeartBeatClient
CURRENT_IP = requests.get('http://api.ipify.org').text
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
log = get_logger("email_notifier", KAFKA_SERVERS)
#MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
EMAIL_CONFIG = json_config_loader('config/email_credentials.json')


def send_email(email_object):
    try:
        # -----------------------------------------------------
        sub = email_object["subject"]
        body = email_object["body"]
        recv_email = email_object["email_id"]
        app_instance_id = email_object["app_instance_id"]
        # -----------------------------------------------------
        log.info(
            f"New email sending request for app_instance_id: {app_instance_id}")
        yag = yagmail.SMTP(EMAIL_CONFIG["mail"], EMAIL_CONFIG["pass"])
        yag.send(
            to=recv_email,
            subject=sub,
            contents=body,
            attachments=None,
        )
        log.info(f'Email sent to {recv_email}')
    except:
        log.error(
            f"Error sending email: reciever: {recv_email} app_instance:{app_instance_id}")


def listener():
    consumer = KafkaConsumer("email_notifier", group_id='email_service', enable_auto_commit=True,
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    log.info('Starting email service')
    try:
        for message in consumer:
            msg = message.value
            try:
                if msg["command"] == "SEND":
                    send_email(msg)
                else:
                    log.error(f'Invalid command issued: {msg}')
            except:
                log.error(' Invalid message scheme')
    except:
        print()
    finally:
        consumer.commit()
        consumer.close()


def decorator():
    self_ip = CURRENT_IP
    print('-------------------------------------------------------------------------')
    print(f' EMAIL SERVICE : {self_ip}')
    print('-------------------------------------------------------------------------')


if __name__ == '__main__':
    decorator()
    listener()
