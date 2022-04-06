from crypt import methods
import pymongo
import os
import logging
import shutil
import zipfile
import requests
from flask import Flask, request, jsonify


app = Flask(__name__)

connection_url="mongodb://20.235.9.68:27017/"
client=pymongo.MongoClient(connection_url)


database_name = "initialiser_db"
app_info = client[database_name]

collection_name = "deployment_nodes"
collection=app_info[collection_name]


@app.route('/initializer/getDeploymentNodes', methods=['GET'])
def getDeploymentNodes():
    cursor = collection.find_one()
    data = cursor["ips"]
    return jsonify({"ips":data})

if __name__ == "__main__":
    app.run(port=5003)