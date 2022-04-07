import logging
from kafka import KafkaConsumer
import json
import socket
from node_agent import startAppDeployment

with open("./config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

def getSelfIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    self_ip = s.getsockname()[0]
    s.close()
    return self_ip


topic = "terminate_" + getSelfIp
sc_consumer = KafkaConsumer(
    topic,
    group_id=cfg["kafka"]["group"],
    bootstrap_servers=cfg["kafka"]["servers"],)
for msg in sc_consumer:
    startAppDeployment(msg.value)