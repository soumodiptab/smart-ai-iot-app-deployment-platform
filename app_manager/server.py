
from flask import Flask, flash, redirect,session, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
from app_db_interaction import auto_matching, validate_app_and_insert, validate_app_instance
import json
import os
import shutil
import sys
import pymongo

from logging import Logger
import logging
import uuid
from pymongo import MongoClient
from app_utils import process_application, save_file_service
from utils import allowed_file_extension
ALLOWED_EXTENSIONS = {'zip', 'rar'}
UPLOAD_FOLDER = 'temp'
# PORT = 8200
log = logging.getLogger('demo-logger')
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY']="secret"


PORT = sys.argv[1]

@app.route('/app/upload', methods=['POST', 'GET'])
def app_type_upload():
    if request.method == "GET":
        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        return render_template('app_upload.html', homeurl=homeurl)
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
            if validate_app_and_insert(relative_file_path):
                  app_id=uuid.uuid4().hex
                  appfilename=str(app_id)+".zip"
                  appfilepath=os.path.join(UPLOAD_FOLDER,appfilename)
                  os.rename(relative_file_path,appfilepath)
                  save_file_service(appfilepath,appfilename)
                
                  flash('Zip File successfully uploaded', 'success')
            else:
                flash('Zip File is not correct', 'errorr')
            shutil.rmtree(UPLOAD_FOLDER)
            return redirect(request.url)
        else:
            flash('Allowed file types are zip,rar', 'errorr')
            return redirect(request.url)


@app.route('/app/display', methods=['GET'])
def app_display():
    
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
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

        url = "http://"
        ip = "127.0.0.1"
        port = "8080"
        homeurl = url + ip + ":" + port+'/'

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["user_db"]  # database_name
        mycol = mydb["users"]  # collection_name

        role_check=list(mycol.find({"username": session['user']}))
        user_role=role_check[0]['role']

        return render_template('display.html', tasks=app_list, homeurl=homeurl, role=user_role)
        
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


@app.route('/app/deploy', methods=['GET', 'POST'])
def app_dep_config():
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

        app_config={
    "app_id": app_id,
    "instances_count": instances_count,
    "geo_loc": {
        "street": street,
        "city": city
    },
    "start_time": start_time,
    "end_time": end_time,
    "periodicity": periodicity,
    "burst_time":burst_time,
    "periodicity_unit": periodicity_unit
                    }
    print(type(app_config))
        
    log.info(f'new request issued: {app_config}')
    if validate_app_instance(app_config):
        if not auto_matching(app_config['app_id'], app_config['geo_loc']):
            flash('Sensors / controllers not present in this location')
        else:
            process_application(app_config,session['user'])
            flash('Application config successfully binded and stored.')
                
            url = "http://"
            ip = "127.0.0.1" 
            port = "8080"
            homeurl = url + ip + ":" + port+'/home'

        return redirect(url_for('app_display'))
    else:
        flash('Invalid application details')
        return redirect(url_for('app_display'))


@app.route('/app/check_app',methods=['GET'])
def check_app():
    app_details=request.json
    client = MongoClient("mongodb://localhost:27017/")
    app_id=app_details['app_id']
    app_instance_id=app_details['app_instance_id']
    #print(client.app_db.instance.count_documents({"app_id": app_id, "app_instance_id": app_instance_id}))
    if client.app_db.instance.count_documents({"app_id": app_id, "app_instance_id": app_instance_id}) > 0:
        
        returnvar={"status":True}
        
        #print(returnvar)
        return returnvar
    else:
        returnvar={"status":False}
        #print(returnvar)
        return returnvar

@app.route('/app/app_instances',methods=['GET'])
def app_instances():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
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
        return render_template('app_instances.html', tasks=app_instance_list)
    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
