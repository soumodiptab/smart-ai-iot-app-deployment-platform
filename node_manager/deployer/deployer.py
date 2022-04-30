# from flask_pymongo import PyMongo
from flask import Flask, request, jsonify

import pymongo
import os
import logging
import shutil
import zipfile
import requests
import json
import yaml
import os
import time
import urllib.request

from kafka import KafkaProducer
from platform_logger import get_logger
from hearbeat_client import HeartBeatClientForService

app = Flask(__name__)


config_file = os.environ.get("DEPLOYER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

log = get_logger('deployer', cfg["kafka"]["address"])

connection_url=cfg["mongo"]["address"]
client=pymongo.MongoClient(connection_url)
database_name = cfg["mongo"]["db"]
app_info = client[database_name]

collection_name = cfg["mongo"]["collection"]
collection=app_info[collection_name]

deploy_producer = KafkaProducer(bootstrap_servers=cfg["kafka"]["address"], 
								value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/deployer/deploy/start', methods=['POST'])
def startDeployment():
	log.info("start deployment")
	app_id = request.form['app_id']
	app_instance_id = request.form['app_instance_id']
	isModel = request.form['isModel']

	print(app_id, app_instance_id, isModel)

	ip = get_deployment_node()
	print(ip)
	isDeployStart = True
	call_deployment_producer(app_id, app_instance_id, isDeployStart, ip, isModel)
	updateAppDeploymentStatus(app_id, app_instance_id, isModel)

	output = {"status" : "Starting app deployment"}

	return jsonify(output), 200

def updateAppDeploymentStatus(app_id, app_instance_id, isModel):
	app_info = {
        "_appId": app_id,
        "app_instance_id": app_instance_id,
        "ip": "",
        "port": "",
        "status": "Pending"
    }
	collection.insert_one(app_info)



@app.route('/deployer/deploy/stop', methods=['POST'])
def stopDeployment():
	data = request.get_json()
	app_id = data['app_id']
	app_instance_id = data['app_instance_id']
	isModel = request.form['isModel']

	ip = get_deployment_node_to_stop(app_id, app_instance_id)
	isDeployStart = False
	call_deployment_producer(app_id, app_instance_id, isDeployStart, ip, isModel)
	output = {"status" : "Stopping app Deployment"}

	return jsonify(output), 200

def call_deployment_producer(app_id, app_instance_id, isDeployStart, ip, is_model):
	print(app_id, app_instance_id, isDeployStart, ip, is_model)
	if isDeployStart:
		log.info("data sent to deploy topic")
		deploy_producer.send("deploy_" + ip, {"app_id" : app_id, "app_instance_id":app_instance_id, "isModel": is_model})
	else:
		deploy_producer.send("termiate_" + ip, {"app_id" : app_id, "app_instance_id":app_instance_id, "isModel": is_model})


	time.sleep(2)

def get_deployment_node():
	address = getServiceAddress("node-manager")
	URL = "http://" + address + "/node-manager/getNewNode"
	r = requests.get(url = URL)
	data = r.json()
	ip = data["ip"]
	return ip

def get_deployment_node_to_stop(app_id, app_instance_id):
	address = getServiceAddress("node-manager")
	URL = "http://" + address + "/node-manager/app/getNode/" + app_id + "/" + app_instance_id 
	r = requests.get(url = URL)
	data = r.json()
	ip = data["ip"]
	port = data["port"]
	return ip

def getServiceAddress(serviceId):
	URL = "http://" + cfg["initialiser"] + "/initialiser/getService/" + serviceId
	r = requests.get(url = URL)
	data = r.json()
	ip = data["ip"]
	port = data["port"]

	address = ip + ":" + port
	return address

def getSelfIp():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    return external_ip

if __name__ == '__main__':
	app.run(host = "0.0.0.0",port=5005, debug=True)
	self_ip = requests.get('https://api.ipify.org').text
	client = HeartBeatClientForService(self_ip, "5005", 'deployer')
	client.start()
