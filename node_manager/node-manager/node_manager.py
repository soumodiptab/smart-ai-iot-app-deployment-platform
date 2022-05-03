from flask import Flask, render_template, request, jsonify

import pymongo
import os
import logging
import shutil
import zipfile
import requests
import yaml
import urllib.request

from queue import PriorityQueue
from platform_logger import get_logger
from heartbeat_client import HeartBeatClientForService

app = Flask(__name__)

config_file = os.environ.get("NODE_MANAGER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

log = get_logger('node-manager', cfg["kafka"]["address"])

connection_url=cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)

database_name = cfg["mongo"]["db"]
app_info = client[database_name]

node_deployment_metadata = cfg["mongo"]["collection"]
collection=app_info[node_deployment_metadata]

node_stats_queue = PriorityQueue()
node_to_stats_dict = {}


@app.route("/")
def home():
    return "hello flask"

@app.route("/node-manager/getNewNode", methods=["GET"])
def getNodeStats():
    global node_stats_queue
    global node_to_stats_dict

    response = requests.get("http://" + cfg["initialiser"] + "/initialiser/getDeploymentNodes")
    json_output = response.json()
    log.info('node-manager {}'.format(json_output))
    
    
    for obj in json_output["ips"]:
        st = "http://" + obj["ip"] + ":" +  obj["port"] + "/node-agent/getNodeStats"
        log.info('', st) 
        resp = requests.get("http://" + obj["ip"] + ":" + obj["port"] + "/node-agent/getNodeStats")
        output = resp.json()
        node_stats_queue.put(output["CPU"], output["RAM"])
        node_to_stats_dict[obj["ip"]] = [output["CPU"],output["RAM"]]
    

    optimal_node = node_stats_queue.get()

    optimal_ip = ""
    for key, value in node_to_stats_dict.items():
        if  value[0] == optimal_node:
            print("optimal ip found")
            optimal_ip = key
            break

    print(optimal_ip)

    payload = {"ip": optimal_ip}
    return jsonify(payload)
    


@app.route("/node-manager/app/getNode/<app_id>/<app_instance_id>", methods=["GET"])
def appDpeloyedNode(app_id, app_instance_id):
    cursor = collection.find_one({"app_id": app_id, "app_instance_id": app_instance_id})
    for doc in cursor:
        deployed_ip = doc["ip"]
        deployed_port = doc["port"]

    out = {"ip": deployed_ip, "port": deployed_port}

    return jsonify(out)


@app.route("/node-manager/getAppUrl/<app_instance_id>", methods=["GET"])
def getAppUrl():
    query = collection.find_one({"app_instance_id":app_instance_id})
    ip_port = {}
    if query['status'] == "success":
        ip_port['ip'] = query['ip']
        ip_port['port'] = query['port']
    return jsonify(ip_port)


def getSelfIp():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
    client = HeartBeatClientForService('node-manager')
    client.start()
