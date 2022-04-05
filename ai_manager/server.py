from asyncio import tasks
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from pathlib import Path
# from kafka import KafkaClient
from werkzeug.utils import secure_filename
import json
from pymongo import MongoClient
import os
import logging
import shutil
import uuid
import sys
from utils import allowed_file_extension
from azure_blob import upload_blob, download_blob
from ai_db_interaction import validate_ai_type, insert_ai_model_info
from generate import generateServer
from utils import copy_files_from_child_to_parent_folder_and_delete_parent_folder, json_config_loader
ALLOWED_EXTENSIONS = {'zip', 'rar'}
# PORT = 6500
log = logging.getLogger('demo-logger')
app = Flask(__name__)
app.secret_key = "secret key"

#PORT = sys.argv[1]
PORT = 6500


@app.route('/model/upload', methods=['POST', 'GET'])
def model_upload():
    if request.method == "GET":
        print("hello")

        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

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
                print("Success!!")
                # # config.json verified
                extract_path = relative_file_path[:-4]

                # generate the Server for AI Model
                # os.system(f'python3 ./generate.py &')
                generateServer(extract_path)

                # Copy from child to parent folder
                sub_folder = extract_path
                parent_folder = Path(sub_folder).parent
                print("Subfolder: " + str(sub_folder) +
                      ", Parent Folder: " + str(parent_folder))
                copy_files_from_child_to_parent_folder_and_delete_parent_folder(
                    str(extract_path)+"/", str(parent_folder)+"/")

                # Zip the model folder
                shutil.make_archive(modelFolder, 'zip', modelFolder)

                # Upload the final zip in AZURE blob storage
                upload_blob(modelId + '.zip')

                # Insert ai_model_info in mongo database
                insert_ai_model_info(modelId, modelFolder)

                # download_blob(modelId + '.zip')

                # Send scheduler_config.json to Deployer through KafkaClient
                scheduler_config = {"Type": "AI Model"}

                flash('Zip File successfully uploaded', 'success')

            else:
                flash('Zip File is not correct', 'error')

            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'error')
            return redirect(request.url)


@app.route('/model/display', methods=['POST', 'GET'])
def model_display():
    try:
        # MONGO_DB_URL = "mongodb://localhost:27017/"
        MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']
        client = MongoClient(MONGO_DB_URL)
        db = client.ai_data
        ai_model_list = []
        Project_List_Col = db.model_info

        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

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

        return render_template('model_display.html', tasks=ai_model_list, homeurl=homeurl)
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)

    # app.run(port=PORT, debug=True, use_debugger=False,
    #         use_reloader=False, passthrough_errors=True)
