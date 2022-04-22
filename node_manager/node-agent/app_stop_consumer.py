import logging
from kafka import KafkaConsumer
import json
import socket
from node_agent import startAppDeployment
from platform_logger import get_logger

node_agent_dir = os.environ.get("NODE_AGENT_HOME") + "/config.yml"
with open(node_agent_dir, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

log = get_logger('app_deployment_consumer', cfg["kafka"]["address"])


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
    bootstrap_servers=cfg["kafka"]["address"],)
for msg in sc_consumer:
    startAppDeployment(msg.value)