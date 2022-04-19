from pymongo import MongoClient
import json
from kafka import KafkaProducer
import time

client = MongoClient("mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client["initialiser_db"]
collection = db["services"]

services = []
for x in collection.find():
  services.append(x["service"])

print(services)
# print("i am here")

# get dynamic ip
ip1 = "20.219.73.70"
ip2 = "20.219.72.194"

def send_message(topic_name, message):
    producer = KafkaProducer(bootstrap_servers=['52.140.57.176:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic_name, message)

no_of_services = len(services)
for i in range(0, len(services), 2):
  data1 = {
  "command":"START",
  "service":services[i]
  }
  data2 = {
  "command":"START",
  "service":services[i+1]
  }
  send_message("service_{}".format(ip1), data1)
  send_message("service_{}".format(ip2), data2)
  print("service_{}".format(ip1))
  print("service_{}".format(ip2))
  time.sleep(2)


