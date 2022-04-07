import logging
from kafka import KafkaConsumer
import json
import socket
import os
import yaml
import urllib.request
from node_agent import startAppDeployment

node_agent_dir = os.environ.get("NODE_AGENT_HOME") + "/config.yml"
with open(node_agent_dir, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

def getSelfIp():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip


#topic = cfg["kafka"]["topic"]
topic = "deloy_" + getSelfIp()
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