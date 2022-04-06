from flask import Flask, render_template, request, jsonify

import pymongo
import os
import logging
import shutil
import zipfile
import requests
from queue import PriorityQueue

app = Flask(__name__)


connection_url="mongodb://172.20.10.2:27017/"
client=pymongo.MongoClient(connection_url)
# print(client.list_database_names())

database_name = "node_manager_db"
app_info = client[database_name]

node_deployment_metadata = "node_deployment_metadata"
collection=app_info[node_deployment_metadata]

node_stats_queue = PriorityQueue()
node_to_stats_dict = {}


@app.route("/")
def home():
    return "hello flask"

# @app.route("/node-manager/getNewNode", methods = ["GET"])
# def getNewNode():
#     resp = requests.get("http://127.0.0.1:5001/node-agent/getNodeStats")
#     return resp.json()

@app.route("/node-manager/getNewNode", methods=["GET"])
def getNodeStats():
    global node_stats_queue
    global node_to_stats_dict

    response = requests.get("http://127.0.0.1:5003/initializer/getDeploymentNodes")
    json_output = response.json()
    print(json_output["ips"])
    
    
    for obj in json_output["ips"]:
        st = "http://" + obj["ip"] + ":" +  obj["port"] + "/node-agent/getNodeStats"
        print(st) 
        resp = requests.get("http://" + obj["ip"] + ":" + obj["port"] + "/node-agent/getNodeStats")
        output = resp.json()
        node_stats_queue.put(output["CPU"], output["RAM"])
        node_to_stats_dict[obj["ip"]] = [output["CPU"],output["RAM"]]
    

    optimal_node = node_stats_queue.get()
    # print(optimal_node)

    # print("here", node_to_stats_dict.get_key(optimal_node))
    optimal_ip = ""
    for key, value in node_to_stats_dict.items():
        if  value[0] == optimal_node:
            print("optimal ip found")
            optimal_ip = key
            break

    print(optimal_ip)

    payload = {"ip": optimal_ip}
    return jsonify(payload)


# @app.route('/node-manager/application/info', methods=['GET'])
# def appInfo():
#     #appInfo = request.get_json()
#     args = request.args
#     appId = args.get('app-id')
#     response = {}
#     response = collection.find_one({"_appId":appId})
#     print(response)
#     return response

# @app.route('/node-manager/deployment/status', methods=['POST'])
# def nodeDeploymentStatus():
#     app_info = {
#     "_appId":request.form['app_id'],
#     "ip":request.form['ip'],
#     "port":request.form['port'],
#     "status":request.form['status']
#     }
#     collection.insert_one(app_info)

#     return jsonify({"status": "Updated metadata successfully",}), 200
    

if __name__ == "__main__":
    app.run(port = 5000)