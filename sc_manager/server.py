from asyncio import tasks
from flask import Flask, flash, redirect, render_template, session, request, jsonify, url_for
from werkzeug.utils import secure_filename
from sc_db_interaction import validate_sc_type_and_insert, validator_sc_instance_and_insert
import json
from bson.json_util import dumps
from pymongo import MongoClient
import os
import sys
from platform_logger import get_logger
import shutil
from utils import allowed_file_extension, json_config_loader
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
log = get_logger('sensor_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# PORT = 8101
INITIALIZER_ADDRESS = json_config_loader('config/initialiser.json')["ADDRESS"]

PORT = sys.argv[1]

import requests 

def getServiceUrl(service_name):
    URL = "http://" + INITIALIZER_ADDRESS + \
        "/initialiser/getService/" + service_name
    r = requests.get(url=URL)
    data = r.json()
    ip = data["ip"]
    port = data["port"]
    url = "http://" + ip + ":" + port
    return url

# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)

MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']


@app.route('/sc_type/upload', methods=['POST', 'GET'])
def sc_type_upload():
    if request.method == "GET":
        client = MongoClient(MONGO_DB_URL)
        db = client.initialiser_db
        sc_ip = db.ips.find_one({"name":"request"})
        #print(sc_ip)
        url = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
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
        client = MongoClient(MONGO_DB_URL)
        db = client.initialiser_db
        sc_ip = db.ips.find_one({"name":"request"})
        #print(sc_ip)
        url = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
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
        
        db = client.initialiser_db
        sc_ip = db.ips.find_one({"name":"request"})
        #print(sc_ip)
        url = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
        homeurl = url + ip + ":" + port+'/'

        app_ip = db.ips.find_one({"name": "app_manager"})
        url1 = "http://"
        ip = app_ip["ip"]
        port = app_ip["port"]
        url1 = url1 + ip + ":" + port+'/'

        ai_ip = db.ips.find_one({"name": "ai_manager"})
        url2 = "http://"
        ip = ai_ip["ip"]
        port = ai_ip["port"]
        url2 = url2 + ip + ":" + port+'/'
        mydb = client["user_db"]  # database_name
        mycol = mydb["users"]  # collection_name

        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        return render_template('display.html', tasks=sc_type_list, role=user_role, homeurl=homeurl, app_url=url1,ai_url=url2)
    except Exception as e:
        log.error({'error': str(e)})

@app.route('/sc_instance/display', methods=['POST', 'GET'])
def sc_instance_display():
    try:
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
        
        db = client.initialiser_db
        sc_ip = db.ips.find_one({"name":"request"})
        #print(sc_ip)
        url = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
        homeurl = url + ip + ":" + port+'/'

        return render_template('display_instance.html', tasks=sc_type_list, homeurl=homeurl)
    except Exception as e:
        log.error({'error': str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
    # app.run(port=PORT, debug=True, use_debugger=False,
    #         use_reloader=False, passthrough_errors=True)
