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

app = Flask(__name__)

APP_ZIP_DIRECTORY = "/home/vishal/Documents/sem2/IAS/integration/temp/"
# APP_ZIP_DIRECTORY = "../temp"

#APP_PREFIX = "app_"

APP_TEMP_DIRECTORY = "/home/vishal/Documents/temp/"
# APP_TEMP_DIRECTORY = "../temp_dir/"


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@app.route("/node-agent/port", methods=["GET"])
def getPort():
    # port = find_free_port()
    to_send = {"ip": "127.0.0.1"}
    # resp = requests.post("http://127.0.0.1:5000/getNewNode", json=to_send)
    return to_send


@app.route("/node-agent/getNodeStats", methods=["GET"])
def getNodeStats():
    l1, l2, l3 = psutil.getloadavg()
    CPU_use = (l3/os.cpu_count()) * 100
    RAM_use = psutil.virtual_memory()[2]
    to_send = {"CPU": str(CPU_use), "RAM": str(RAM_use), "Status": "1"}
    return to_send


@app.route("/node-agent/deploy", methods=["POST"])
def deployApp():
    app_id = request.form['app_id']
    # print(data)
    # app_id = data['app_id']

    # app_zip_full_path = APP_ZIP_DIRECTORY + APP_PREFIX + app_id + ".zip"
    app_zip_full_path = APP_ZIP_DIRECTORY + app_id + ".zip"
    print(app_zip_full_path)
    app_temp_dest_path = APP_TEMP_DIRECTORY + app_id + "/"

    if not os.path.isfile(app_zip_full_path):
        print("App Zip not found in DB")
        # logging.error("Application" + app_id + " not found in DB")
        return 0

    isExist = os.path.exists(APP_TEMP_DIRECTORY)
    if not isExist:
        os.makedirs(APP_TEMP_DIRECTORY)

    isExist = os.path.exists(app_temp_dest_path)
    if not isExist:
        os.makedirs(app_temp_dest_path)

    with zipfile.ZipFile(app_zip_full_path, "r") as zip_ref:
        zip_ref.extractall(app_temp_dest_path)

    req_file_path = app_temp_dest_path + "app/requirements.txt"

    req_installation_data = subprocess.Popen(
        ['pip', 'install', '-r', req_file_path], stdout=subprocess.PIPE)
    req_installation_output = req_installation_data.communicate()
    print(str(req_installation_output))

    # run_app_server_data = subprocess.Popen(['nohup', app_temp_dest_path + 'server.py', '&'])
    # run_app_output = run_app_server_data.communicate()
    # print(str(run_app_output))

    os.system("python3 " + app_temp_dest_path + "app/app.py &")

    port = find_free_port()
    return jsonify({"ip": "127.0.0.1", "port": str(port), "app_id": app_id, "status": "Success", }), 200


if __name__ == "__main__":
    app.run(port=5001)
