from flask import Flask, render_template, request, jsonify

import pymongo
import os
import logging
import shutil
import zipfile
import requests

app = Flask(__name__)


connection_url="mongodb://localhost:27017/"
client=pymongo.MongoClient(connection_url)
# print(client.list_database_names())

database_name = "node_manager_db"
app_info = client[database_name]

collection_name = "node_metadata"
collection=app_info[collection_name]


@app.route("/")
def home():
    return "hello flask"

@app.route("/node-manager/getNewNode", methods = ["GET"])
def getNewNode():
    """Will return ip address and port pn which application will be deployed"""
    resp = requests.get("http://127.0.0.1:5001/node-agent/port")
    print(resp.json())
    # status = {"ip":"127.0.0.1", "port":str(port)}
    return resp.json()

@app.route("/node-manager/getNodeStats", methods=["GET"])
def getNodeStats():
    try:
        resp = requests.get("http://127.0.0.1:5001/node-agent/getNodeStats")
        return resp.json()
    except:

        return {"status":"0"}

@app.route('/node-manager/application/info', methods=['GET'])
def appInfo():
    #appInfo = request.get_json()
    args = request.args
    appId = args.get('app-id')
    response = {}
    response = collection.find_one({"_appId":appId})
    print(response)
    return response

@app.route('/node-manager/deployment/status', methods=['POST'])
def nodeDeploymentStatus():
    app_info = {
    "_appId":request.form['app_id'],
    "ip":request.form['ip'],
    "port":request.form['port'],
    "status":request.form['status']
    }
    collection.insert_one(app_info)

    return jsonify({"status": "Updated metadata successfully",}), 200
    

if __name__ == "__main__":
    app.run(port = 5000)