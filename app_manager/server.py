
import requests
from flask import Flask, flash, redirect, session, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from app_db_interaction import auto_matching_check, validate_app_and_insert, validate_app_instance
import json
import os
import shutil
import sys
import pymongo
from generate import generateDockerFile
from logging import Logger
import logging
import uuid
from pymongo import MongoClient
from platform_logger import get_logger
from app_utils import process_application, save_file_service
from utils import allowed_file_extension, json_config_loader
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
log = get_logger('app_manager', json_config_loader(
    'config/kafka.json')["bootstrap_servers"])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'

# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)

MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']

INITIALIZER_ADDRESS = json_config_loader('config/initialiser.json')["ADDRESS"]

PORT = sys.argv[1]
#PORT = 8200


def find_session():
    mongo_client = MongoClient(MONGO_DB_URL)
    session_inst = mongo_client.session_db.session_data
    if session_inst.count_documents({}) > 0:
        session['user'] = session_inst.find_one({})['user']
        return True
    else:
        return False


def getServiceUrl(service_name):
    URL = "http://" + INITIALIZER_ADDRESS + \
        "/initialiser/getService/" + service_name
    r = requests.get(url=URL)
    data = r.json()
    ip = data["ip"]
    port = data["port"]
    url = "http://" + ip + ":" + port
    return url


@app.route('/app/upload', methods=['POST', 'GET'])
def app_type_upload():
    find_session()
    if request.method == "GET":
        client = MongoClient(MONGO_DB_URL)
        db = client.initialiser_db
        request_ip = db.running_services.find_one(
            {"service": "request_manager"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        homeurl = url + ip + ":" + port+'/'

        ai_ip = db.running_services.find_one({"service": "ai_manager"})
        # print(sc_ip)
        url1 = "http://"
        ip = ai_ip["ip"]
        port = ai_ip["port"]
        url1 = url1 + ip + ":" + port+'/'

        sc_ip = db.running_services.find_one({"service": "sc_manager"})
        # print(sc_ip)
        url2 = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
        url2 = url2 + ip + ":" + port+'/'
        mydb = client["user_db"]  # database_name
        mycol = mydb["users"]  # collection_name

        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        client.close()
        return render_template('app_upload.html', homeurl=homeurl, role=user_role, ai_url=url1, sc_url=url2)
    else:
        if 'file' not in request.files:
            flash('No file part', 'info')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading', 'info')
            return redirect(request.url)
        if file and allowed_file_extension(file.filename, ALLOWED_EXTENSIONS):
            #filename = secure_filename(file.filename)
            app_id = uuid.uuid4().hex
            filename = secure_filename(app_id+".zip")
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
            relative_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(relative_file_path)
            if validate_app_and_insert(app_id, relative_file_path):
                generateDockerFile(relative_file_path)
                shutil.make_archive(
                    relative_file_path[:-4], 'zip', relative_file_path[:-4])
                appfilename = app_id+".zip"
                appfilepath = os.path.join(UPLOAD_FOLDER, appfilename)
                os.rename(relative_file_path, appfilepath)
                save_file_service(appfilepath, appfilename)
                flash('Zip File successfully uploaded', 'success')
            else:
                flash('Zip File is not correct', 'error')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'errorr')
            return redirect(request.url)


@app.route('/app/display', methods=['GET'])
def app_display():
    find_session()
    try:
        client = MongoClient(MONGO_DB_URL)
        app_list = []
        for app_record in client.app_db.app.find():
            display_record = {
                "app_id": app_record["app_id"],
                "app_name": app_record["app_name"],
                "description": app_record["description"],
                "script": app_record["script"],
                "controller": app_record["controller"],
                "sensor": app_record["sensor"],
                "model": app_record["model"],
                "database": app_record["database"],
                "sensors": app_record["sensors"],
                "controllers": app_record["controllers"],
                "models": app_record["models"]

            }
            app_list.append(display_record)
            log.info(app_list)

        db = client.initialiser_db
        request_ip = db.running_services.find_one(
            {"service": "request_manager"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        homeurl = url + ip + ":" + port+'/'

        ai_ip = db.running_services.find_one({"service": "ai_manager"})
        # print(sc_ip)
        url1 = "http://"
        ip = ai_ip["ip"]
        port = ai_ip["port"]
        url1 = url1 + ip + ":" + port+'/'

        sc_ip = db.running_services.find_one({"service": "sc_manager"})
        # print(sc_ip)
        url2 = "http://"
        ip = sc_ip["ip"]
        port = sc_ip["port"]
        url2 = url2 + ip + ":" + port+'/'

        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["user_db"]  # database_name
        # mycol = mydb["users"]  # collection_name

        mydb = client["user_db"]  # database_name
        mycol = mydb["users"]  # collection_name

        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        client.close()
        return render_template('display.html', tasks=app_list, homeurl=homeurl, role=user_role, ai_url=url1, sc_url=url2)

    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


@app.route('/app/deploy', methods=['GET', 'POST'])
def app_dep_config():
    find_session()
    if request.method == "GET":
        return render_template('scheduling_form.html', app_id=request.args.get('appid'))
    else:
        #app_config = json.loads(request.get_json())

        print(request.form['app_id'])

        app_id = request.form["app_id"]
        instances_count = request.form["instances_count"]
        street = request.form["street"]
        city = request.form["city"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]
        periodicity = request.form["periodicity"]
        burst_time = request.form["burst_time"]
        periodicity_unit = request.form["periodicity_unit"]

        app_config = {
            "app_id": app_id,
            "instances_count": instances_count,
            "geo_loc": {
                "street": street,
                "city": city
            },
            "start_time": start_time,
            "end_time": end_time,
            "periodicity": periodicity,
            "burst_time": burst_time,
            "periodicity_unit": periodicity_unit
        }
    print(type(app_config))
    log.info(f'new request issued: {app_config}')
    if validate_app_instance(app_config):
        if not auto_matching_check(app_config['app_id'], app_config['geo_loc']):
            flash('Sensors / controllers not present in this location')
            return redirect(request.referrer)
        else:
            process_application(app_config, session['user'])
            flash('Application config successfully binded and stored.')
            client = MongoClient(MONGO_DB_URL)
            db = client.initialiser_db
            request_ip = db.running_services.find_one({"name": "ai_manager"})
            # print(request_ip)
            url = "http://"
            ip = request_ip["ip"]
            port = request_ip["port"]
            homeurl = url + ip + ":" + port+'/home'
            client.close()
            return redirect(url_for('app_display'))
    else:
        flash('Invalid application details')
        return redirect(url_for('app_display'))


@app.route('/app/check_app', methods=['GET'])
def check_app():
    find_session()
    client = MongoClient(MONGO_DB_URL)
    app_details = request.json
    # client = MongoClient("mongodb://localhost:27017/")
    app_id = app_details['app_id']
    app_instance_id = app_details['app_instance_id']
    #print(client.app_db.instance.count_documents({"app_id": app_id, "app_instance_id": app_instance_id}))
    if client.app_db.instance.count_documents({"app_id": app_id, "app_instance_id": app_instance_id}) > 0:

        returnvar = {"status": True}
        client.close()
        # print(returnvar)
        return returnvar
    else:
        returnvar = {"status": False}
        client.close()
        # print(returnvar)
        return returnvar


@app.route('/app/app_instances', methods=['GET'])
def app_instances():
    find_session()
    try:
        client = MongoClient(MONGO_DB_URL)
        app_instance_list = []
        for app_instance_record in client.app_db.instance.find():
            display_record = {
                "app_id": app_instance_record["app_id"],
                "app_instance_id": app_instance_record["app_instance_id"],
                "end_user": app_instance_record["end_user"],
                "sensors": app_instance_record["sensors"],
                "controllers": app_instance_record["controllers"],
                "models": app_instance_record["models"],
            }
            app_instance_list.append(display_record)
            log.info(app_instance_list)
            client.close()
        return render_template('app_instances.html', tasks=app_instance_list)
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
    # app.run(port=PORT, debug=True, use_debugger=False,
    #         use_reloader=False, passthrough_errors=True)
