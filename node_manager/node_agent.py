from contextlib import closing
import socket
from crypt import methods
from operator import imod
from flask import Flask, render_template, request, jsonify
import os
import psutil
import json
import zipfile
import shutil
import subprocess
import socket
import asyncio
import threading

app = Flask(__name__)


#APP_PREFIX = "app_"

APP_TEMP_DIRECTORY = "/home/vishal/Documents/temp/"
# APP_TEMP_DIRECTORY = "../temp_dir/"


def consumeDeploymentData():
    print("started deployment consumer")
    try:
        self_ip = getSelfIp()
        consumer = KafkaConsumer("deploy_" + self_ip,bootstrap_servers=['13.71.109.62:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        print(consumer)
        for msg in consumer:    
            print("consuming")
            msg = message.value
            app_id = msg["app_id"]
            app_instance_id = msg["app_instance_id"]
            is_model = msg["isModel"]

            if is_model:
                getAppZipFromStorage(app_id, "aibucket")
            else:
                getAppZipFromStorage(app_id, "appbucket")

            updateNodeDeploymentStatus(app_id, app_instance_id, self_ip, free_port, "Success")

    except:
         print("Error!!")


def getSelfIp():   
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname) 

    return IPAddr

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


# @app.route("/node-agent/port", methods=["GET"])
# def getPort():
#     # port = find_free_port()
#     to_send = {"ip": "127.0.0.1"}
#     # resp = requests.post("http://127.0.0.1:5000/getNewNode", json=to_send)
#     return to_send


@app.route("/node-agent/getNodeStats", methods=["GET"])
def getNodeStats():
    l1, l2, l3 = psutil.getloadavg()
    CPU_use = (l3/os.cpu_count()) * 100
    RAM_use = psutil.virtual_memory()[2]
    to_send = {"CPU": str(CPU_use), "RAM": str(RAM_use), "Status": "1"}
    return to_send

# async def deployApp():
#     # app_id = request.form['app_id']
#     # app_instance_id = request.form['app_instance_id']
#     # ip = request.form['ip']
#     # print(data)
#     # app_id = data['app_id']
#     print("inside async")
#     self_ip = getSelfIp()
#     consumer = KafkaConsumer("deploy_" + self_ip,bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))

#     for message in consumer:
#         print("consuming")
#         msg = message.value
#         app_id = msg["app_id"]
#         app_instance_id = msg["app_instance_id"]
#         is_model = msg["isModel"]


#     if is_model:
#         getAppZipFromStorage(app_id, "aibucket")
#     else:
#         getAppZipFromStorage(app_id, "appbucket")

#     # app_zip_full_path = APP_ZIP_DIRECTORY + APP_PREFIX + app_id + ".zip"
#     # app_zip_full_path = APP_ZIP_DIRECTORY + app_id + ".zip"
#     # print(app_zip_full_path)
#     # app_temp_dest_path = APP_TEMP_DIRECTORY + app_id + "/"

#     # if not os.path.isfile(app_zip_full_path):
#     #     print("App Zip not found in DB")
#     #     # logging.error("Application" + app_id + " not found in DB")
#     #     return 0

#     # isExist = os.path.exists(APP_TEMP_DIRECTORY)
#     # if not isExist:
#     #     os.makedirs(APP_TEMP_DIRECTORY)

#     # isExist = os.path.exists(app_temp_dest_path)
#     # if not isExist:
#     #     os.makedirs(app_temp_dest_path)

#     # with zipfile.ZipFile(app_zip_full_path, "r") as zip_ref:
#     #     zip_ref.extractall(app_temp_dest_path)

#     # req_file_path = app_temp_dest_path + "app/requirements.txt"

#     # req_installation_data = subprocess.Popen(
#     #     ['pip', 'install', '-r', req_file_path], stdout=subprocess.PIPE)
#     # req_installation_output = req_installation_data.communicate()
#     # print(str(req_installation_output))

#     # free_port = find_free_port()
#     # os.system("python3 " + app_temp_dest_path + "app/app.py " + free_port + " &")


    


def updateNodeDeploymentStatus(app_id, app_instance_id, ip, port, status):
    app_info = {
    "_appId":app_id,
    "app_instance_id":app_instance_id,
    "ip":ip,
    "port":port,
    "status":status
    }
    collection.insert_one(app_info)


def getAppZipFromStorage(app_id, bucket_name):
    try:
        service = ShareFileClient.from_connection_string(conn_str="https://iasprojectaccount.file.core.windows.net/DefaultEndpointsProtocol=https;AccountName=iasprojectstorage;AccountKey=Ucp2Z0KRhHdAgt9pb9+Goe31IWJsBmH44PlPK6fB4eKIoHIvYya3BmCwNMhatGM0yvZH3TBMcaj6JvIk8J3kJA==;EndpointSuffix=core.windows.net", share_name=bucket_name, file_path=app_id + ".zip")
    except:
        print("File not present")

    zip_file_name = "{}.zip".format(app_id)
    with open(zip_file_name, "wb") as file_handle:
        data = service.download_file()
        data.readinto(file_handle)
    unzip_run_app(zip_file_name, app_id)

def unzip_run_app(app_zip_file, app_id):
    app_zip_full_path = APP_ZIP_DIRECTORY + app_zip_file
    
    with(app_zip_file, "r") as zipobj:
        zipobj.extractAll()
        #print('mayank')

    req_file_path =  app_id + "/requirements.txt"
    req_installation_data = subprocess.Popen(['pip', 'install', '-r', req_file_path], stdout=subprocess.PIPE)
    req_installation_output = req_installation_data.communicate()

    #extra_scripts = "config"
    os.system("python3 " + app_id + "/server.py &")

    # os.chdir('config')

    data = json.load('config/control.json')
    for i in data['scripts']:
        os.system("python3" + i['filename'] + " " +  i['args'] + "&")




if __name__ == "__main__":
    t1 = threading.Thread(target=consumeDeploymentData, args=())
    t1.start()
    # t1.join()
    app.run(port=5001)
