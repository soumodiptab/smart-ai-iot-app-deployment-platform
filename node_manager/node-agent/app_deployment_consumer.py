import logging
from kafka import KafkaConsumer
import json
import socket
import os
import yaml
from node_agent import startAppDeployment

node_agent_dir = os.environ.get("NODE_AGENT_HOME") + "/config.yml"
with open(node_agent_dir, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

def getSelfIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    self_ip = s.getsockname()[0]
    s.close()
    return self_ip


topic = cfg["kafka"]["topic"]
print(topic)
print(cfg["kafka"]["servers"])
sc_consumer = KafkaConsumer(
    topic,
    group_id=cfg["kafka"]["group"],
    bootstrap_servers=cfg["kafka"]["servers"],)
for msg in sc_consumer:
    print(msg.value)
    deployment_msg_from_deployer = json.loads(msg.value.decode('utf-8'))
    startAppDeployment(deployment_msg_from_deployer)