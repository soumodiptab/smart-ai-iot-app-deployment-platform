from re import M
from asyncio import tasks
from flask import Flask, current_app, flash, redirect, render_template, session, request, jsonify, url_for
from pathlib import Path
# from kafka import KafkaClient
from werkzeug.utils import secure_filename
import json
from platform_logger import get_logger
from pymongo import MongoClient
from datetime import datetime
import pytz
import os
import logging
import shutil
import uuid
import sys
import requests
from utils import allowed_file_extension, send_message, getCurrentTimeInIST, getFutureTimeInIST
from azure_blob import upload_blob, download_blob
from ai_db_interaction import validate_ai_type, insert_ai_model_info
from generate import generateServer, generateDockerFile
from utils import copy_files_from_child_to_parent_folder_and_delete_child_folder, json_config_loader
from heartbeat_client import HeartBeatClientForService
ALLOWED_EXTENSIONS = {'zip', 'rar'}
# PORT = 6500
log = get_logger('ai_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
#CORS(app, supports_credentials=True)
# CORS(app)
MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']

#PORT = sys.argv[1]
PORT = 6500


@app.route('/model/upload', methods=['POST', 'GET'])
def model_upload():
    find_session()
    if request.method == "GET":
        print("hello")
        client = MongoClient(MONGO_DB_URL)
        db = client.initialiser_db
        request_ip = db.running_services.find_one(
            {"service": "request_manager"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        homeurl = url + ip + ":" + port+'/'
        client.close()
        return render_template('model_upload.html', homeurl=homeurl)
    else:
        UPLOAD_FOLDER = modelFolder = modelId = uuid.uuid4().hex
        if 'file' not in request.files:
            flash('No file part', 'info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', 'info')
            return redirect(request.url)
        if file and allowed_file_extension(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            relative_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(relative_file_path)

            if validate_ai_type(relative_file_path):
                log.info("Model validated")
                # # config.json verified
                extract_path = relative_file_path[:-4]

                # generate the Server for AI Model
                # os.system(f'python3 ./generate.py &')
                generateServer(extract_path)

                generateDockerFile(extract_path)

                # os.system(f'pipreqs {extract_path} --force')
                # log.info('Generating requirements.txt')

                # Copy from child to parent folder
                sub_folder = extract_path
                parent_folder = Path(sub_folder).parent
                print("Subfolder: " + str(sub_folder) +
                      ", Parent Folder: " + str(parent_folder))
                copy_files_from_child_to_parent_folder_and_delete_child_folder(
                    str(extract_path)+"/", str(parent_folder)+"/")

                # copy the requirements2.txt in the modelFolder
                shutil.copy("requirementsDS.txt", modelFolder)

                # Zip the model folder
                shutil.make_archive(modelFolder, 'zip', modelFolder)

                # Upload the final zip in AZURE blob storage
                upload_blob(modelId + '.zip')

                # Insert ai_model_info in mongo database
                insert_ai_model_info(modelId, modelFolder)

                # Delete the zip from system
                os.remove(modelId + '.zip')

                # download_blob(modelId + '.zip')

                # Send scheduler_config.json to Deployer through KafkaClient
                # appId is actually modelId
                # scheduler_config = {"modelId": modelId, "isModel": True}
                # send_message('scheduler', scheduler_config)

                # Set the delay to 2 mins
                delay = 2
                futureTimeIST = getFutureTimeInIST(delay)

                scheduler_config = {"message_type": "SCHED_APP",
                                    "app_id": modelId, "isModel": True,
                                    "app_instance_id": modelId,
                                    "start_time": futureTimeIST,
                                    "end_time": "00:00", "periodicity": "5", "burst_time": "1", "periodicity_unit": "Hrs"}
                send_message('scheduler', scheduler_config)

                flash('Zip File successfully uploaded', 'success')

            else:
                flash('Zip File is not correct', 'error')

            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'error')
            return redirect(request.url)


def find_session():
    mongo_client = MongoClient(MONGO_DB_URL)
    session_inst = mongo_client.session_db.session_data
    if session_inst.count_documents({}) > 0:
        session['user'] = session_inst.find_one({})['user']
        return True
    else:
        return False


@app.route('/model/display', methods=['POST', 'GET'])
def model_display():
    try:
        find_session()
        # MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        db = client.ai_data
        ai_model_list = []
        Project_List_Col = db.model_info
        db = client.initialiser_db
        request_ip = db.running_services.find_one(
            {"service": "request_manager"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        homeurl = url + ip + ":" + port+'/'

        app_ip = db.running_services.find_one({"service": "app_manager"})
        url1 = "http://"
        ip = app_ip["ip"]
        port = app_ip["port"]
        url1 = url1 + ip + ":" + port+'/'

        sc_ip = db.running_services.find_one({"service": "sc_manager"})
        url2 = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
        url2 = url2 + ip + ":" + port+'/'

        mydb = client["user_db"]  # database_name
        mycol = mydb["users"]  # collection_name

        print(session)

        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        for model_record in list(Project_List_Col.find()):
            display_record = {
                "modelId": model_record["modelId"],
                "modelName": model_record["modelName"],
                "deployedIP": model_record["deployedIp"],
                "PORT": model_record["port"],
                "runningStatus": model_record["runningStatus"],
                "input": model_record["config"]["preprocessing"]["input_params"],
                "output": model_record["config"]["postprocessing"]["output_params"]
            }
            ai_model_list.append(display_record)
        client.close()
        return render_template('model_display.html', tasks=ai_model_list, role=user_role, homeurl=homeurl, app_url=url1, sc_url=url2)
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


if __name__ == '__main__':
    heartbeat_client = HeartBeatClientForService('ai_manager')
    heartbeat_client.start()
    app.run(host="0.0.0.0", port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
