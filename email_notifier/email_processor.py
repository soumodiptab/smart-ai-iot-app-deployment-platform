import os
import json
from pymongo import MongoClient
from platform_logger import get_logger
from utils import json_config_loader
from kafka import KafkaConsumer
import requests
import smtplib
import ssl
from heartbeat_client import HeartBeatClient
CURRENT_IP = requests.get('http://api.ipify.org').text
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
service_topic = "service"+"_"+CURRENT_IP
log = get_logger(service_topic, KAFKA_SERVERS)
MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']


def send_email(email_object):
    try:
        #-----------------------------------------------------
        subject = email_object["subject"]
        body = email_object["body"]
        email_id = email_object["email_id"]
        app_instance_id = email_object["app_instance_id"]
        #-----------------------------------------------------

        log.info(
            f"New email sending request for app_instance_id: {app_instance_id}")
    except:
        log.error("Invalid email object")


def listener():
    consumer = KafkaConsumer(service_topic, group_id='email_service',
                             bootstrap_servers=KAFKA_SERVERS, value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    log.info('Starting email service')
    for message in consumer:
        msg = message.value
        try:
            if msg["command"] == "SEND":
                send_email(msg["service"])
            else:
                log.error(f'Invalid command issued: {msg}')
        except:
            log.error(' Invalid message scheme')


def decorator():
    self_ip = CURRENT_IP
    print('-------------------------------------------------------------------------')
    print(f' EMAIL SERVICE : {self_ip}')
    print('-------------------------------------------------------------------------')

if __name__ == '__main__':
    decorator()
    listener()
