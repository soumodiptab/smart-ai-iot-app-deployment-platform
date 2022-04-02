# from flask_pymongo import PyMongo
from flask import Flask, request, jsonify

import pymongo
import os
import logging
import shutil
import zipfile
import requests

from kafka import KafkaProducer

app = Flask(__name__)

# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/deployment_metadata")
# db = deployment_metadata.db

connection_url="mongodb://localhost:27017/"
client=pymongo.MongoClient(connection_url)
database_name = "deployer_db"
app_info = client[database_name]

collection_name = "deployment_metadata"
collection=app_info[collection_name]

logging.basicConfig(filename='deployer.log', filemode='w', 
					format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
					datefmt='%d-%b-%y %H:%M:%S')


deploy_producer = KafkaProducer(bootstrap_servers=[
                        'localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

terminator_producer = KafkaProducer(bootstrap_servers=[
                     	'localhost:9093'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/deployer/deploy/start', methods=['POST'])
def startDeployment():
	# data = request.get_json()
	app_id = request.form['app_id']
    app_instance_id = request.form['app_instance_id']
    isModel = request.form['is_model']

	ip = get_deployment_node()
	isDeployStart = True
	call_deployment_producer(app_id, app_instance_id, isDeployStart, ip, isModel)

	output = {"status" : "Starting app deployment"}

	return jsonify(output), 200


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
	if isDeployStart:
		deplpoy_producer.send(ip, {"app_id" : app_id, "app_instance_id":app_instance_id, "is_model": is_model})
    else:
		terminator_producer.send(ip, {"app_id" : app_id, "app_instance_id":app_instance_id, "is_model": is_model})




# @app.route('/deployer/deploy', methods=['POST'])
# def getPassengerStatus():
# 	data = request.get_json()
	
# 	# Get app id from application manager
# 	app_id = data['app_id']

# 	# print("transferring app zip to temp dir")
# 	# if not transferAppZipToTemp(app_id):
# 	# 	logging.error("transferAppZipToTemp(): Failed to transfer App Zip to Temp Directory")
# 	# 	return jsonify({"error": "Internal Server Error",}), 500

# 	ip = get_deployment_node()
# 	deployment_status = start_deployment(ip)
# 	send_deployment_status = send_deployment_status_to_node_manager(deployment_status)
# 	update_deployment_metadata(deployment_status)

# 	return jsonify({"status": "Deployment Successful",}), 200
	

def get_deployment_node():
	URL = "http://127.0.0.1:5000/node-manager/getNewNode"
	r = requests.get(url = URL)
	data = r.json()
	ip = data['ip']
	return ip

def get_deployment_node_to_stop(app_id, app_instance_id):
	URL = "http://127.0.0.1:5000/node-manager/getNewNode"
	r = requests.get(url = URL)
	data = r.json()
	ip = data['ip']
	return ip

# def start_deployment(ip, app_id):
# 	URL = "http://127.0.0.1:5001/node-agent/deploy"
# 	data = {"app_id" : app_id}
# 	response = requests.post(URL, data = data)
# 	print(response.text)
# 	return response.json()

# def send_deployment_status_to_node_manager(deployment_status):
# 	URL = "http://127.0.0.1:5000/node-manager/deployment/status"
# 	response = requests.post(URL, data = deployment_status)

# def update_deployment_metadata(deployment_status):
# 	print(type(deployment_status))
# 	collection.insert_one(deployment_status)


if __name__ == '__main__':
	app.run(port=5002, debug=True)




