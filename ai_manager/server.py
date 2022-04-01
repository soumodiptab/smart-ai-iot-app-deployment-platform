from asyncio import tasks
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from pathlib import Path
from werkzeug.utils import secure_filename
import json
from bson.json_util import dumps
from pymongo import MongoClient
import os
import logging
import shutil
import uuid
from utils import allowed_file_extension
from ai_db_interaction import validate_ai_type, insert_ai_model_info
from generate import generateServer
from utils import copy_files_from_child_to_parent_folder_and_delete_parent_folder
ALLOWED_EXTENSIONS = {'zip', 'rar'}
PORT = 6500
log=logging.getLogger('demo-logger')
app = Flask(__name__)
app.secret_key = "secret key"


@app.route('/model/upload', methods=['POST', 'GET'])
def model_upload():
    if request.method == "GET":
        print("hello")
        return render_template('model_upload.html')
    else:
        UPLOAD_FOLDER = modelFolder = modelId = uuid.uuid4().hex
        if 'file' not in request.files:
            flash('No file part','info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading','info')
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
                print("Subfolder: " + str(sub_folder) + ", Parent Folder: " + str(parent_folder))
                copy_files_from_child_to_parent_folder_and_delete_parent_folder(str(extract_path)+"/", str(parent_folder)+"/")

                # Zip the model folder
                shutil.make_archive(modelFolder, 'zip', modelFolder)

                # Insert ai_model_info in database
                insert_ai_model_info(modelId, modelFolder)

                flash('Zip File successfully uploaded','success')

                # # 


            else:
                flash('Zip File is not correct','error')

            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar','error')
            return redirect(request.url)



@app.route('/model_type/display', methods=['POST', 'GET'])
def sc_type_display():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        db = client.sc_db
        sc_type_list=[]
        Project_List_Col = db.sc_type
        for sc_type_record in list(Project_List_Col.find()):
            display_record={
                "company":sc_type_record["company"],
                "model": sc_type_record["model"],
                "parameter_count":sc_type_record["parameter_count"],
                "parameters":sc_type_record["parameters"],
                "device":sc_type_record["device"],
                "type":sc_type_record["type"]
            }
            sc_type_list.append(display_record)
            print(sc_type_list)
        return render_template('dmodel_isplay.html',tasks=sc_type_list)
    except Exception as e:
        log.error({'error': str(e)})


if __name__ == '__main__':
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)