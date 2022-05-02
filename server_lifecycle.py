
from pymongo import MongoClient
import json
from kafka import KafkaProducer
import time
from flask import Flask, request, jsonify


client = MongoClient(
    "mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client["initialiser_db"]
collection = db["services"]

services = []
for x in collection.find():
    services.append(x["service"])

# services = set(services)
print(services)
# print("i am here")

# get dynamic ip
# ip1 = "52.140.61.100"
ip1 = "104.211.205.232"
ip2 = "52.172.3.77"
ip3 = "104.211.227.22"


def send_message(topic_name, message):
    producer = KafkaProducer(bootstrap_servers=[
                             '52.172.25.250:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic_name, message)


no_of_services = len(services)
for i in range(0, len(services)):
    data1 = {
        "command": "START",
        "service": services[i]
    }

    if i % 3==0:
        send_message("service_{}".format(ip1), data1)
        print("service_{}".format(ip1), services[i])
    elif i%3==1:
        send_message("service_{}".format(ip2), data1)
        print("service_{}".format(ip2), services[i])
    else:
        send_message("service_{}".format(ip3), data1)
        print("service_{}".format(ip3), services[i])
    
    time.sleep(2)




app = Flask(__name__)

collection1 = db["running_services"]


@app.route('/initialiser/getService/<serviceName>', methods=['GET'])
def getServiceAddress(serviceName):
    # print("hello")
    doc = collection1.find_one({"service": serviceName})
    ip = doc["ip"]
    port = doc["port"]
    return jsonify({"ip": ip, "port": port})



@app.route('/initialiser/getDeploymentNodes', methods=['GET'])
def getDeploymentNodes():
    cursor = collection1.find({"type": "node-agent"})
    node_agent_addresses = []
    for doc in cursor:
        node_agent_address = {}
        node_agent_address["ip"] = doc['ip']
        node_agent_address["port"] = doc['port']
        node_agent_addresses.append(node_agent_address)
    return jsonify({"ips": node_agent_addresses})





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
