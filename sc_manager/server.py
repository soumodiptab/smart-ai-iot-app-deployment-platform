from asyncio import tasks
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from sc_db_interaction import validate_sc_type_and_insert, validator_sc_instance_and_insert
import json
from bson.json_util import dumps
from pymongo import MongoClient
import os
from platform_logger import get_logger
import shutil
from utils import allowed_file_extension, json_config_loader
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
PORT = 8101
log = get_logger('sensor_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/sc_type/upload', methods=['POST', 'GET'])
def sc_type_upload():
    if request.method == "GET":

        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        return render_template('sc_type_upload.html', homeurl=homeurl)
    else:
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
            if validate_sc_type_and_insert(relative_file_path):
                flash('Zip File successfully uploaded', 'success')
            else:
                flash('Zip File is not correct', 'error')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'error')
            return redirect(request.url)


@app.route('/sc_instance/upload', methods=['POST', 'GET'])
def sc_instance_upload():
    if request.method == "GET":

        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        return render_template('sc_instance_upload.html', homeurl=homeurl)
    else:
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
            if validator_sc_instance_and_insert(relative_file_path):
                flash('Zip File successfully uploaded', 'success')
            else:
                flash('Zip File is not correct', 'error')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'error')
            return redirect(request.url)


@app.route('/sc_type/display', methods=['POST', 'GET'])
def sc_type_display():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        db = client.sc_db
        sc_type_list = []
        Project_List_Col = db.sc_type
        for sc_type_record in list(Project_List_Col.find()):
            display_record = {
                "company": sc_type_record["company"],
                "model": sc_type_record["model"],
                "parameter_count": sc_type_record["parameter_count"],
                "parameters": sc_type_record["parameters"],
                "device": sc_type_record["device"],
                "type": sc_type_record["type"]
            }
            sc_type_list.append(display_record)
            log.info(sc_type_list)
        
        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        return render_template('display.html', tasks=sc_type_list, homeurl=homeurl)
    except Exception as e:
        log.error({'error': str(e)})

@app.route('/sc_instance/display', methods=['POST', 'GET'])
def sc_instance_display():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        db = client.sc_db
        sc_type_list = []
        Project_List_Col = db.sc_instance
        for sc_type_record in list(Project_List_Col.find()):
            display_record = {
                "type": sc_type_record["type"],
                "ip_loc": sc_type_record["ip_loc"],
                "geo_location": sc_type_record["geo_location"],
                "device": sc_type_record["device"]
            }
            sc_type_list.append(display_record)
            log.info(sc_type_list)
        
        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        return render_template('display_instance.html', tasks=sc_type_list, homeurl=homeurl)
    except Exception as e:
        log.error({'error': str(e)})


if __name__ == '__main__':
    # app.run(host="0.0.0.0",port=PORT, debug=True, use_debugger=False,
    #         use_reloader=False, passthrough_errors=True)
    
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
