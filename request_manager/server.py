from flask import Flask, render_template, session, request, redirect, url_for, flash
from logging import Logger
import logging
import sys
from pymongo import MongoClient
from utils import json_config_loader
import requests

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["user_db"]  # database_name
# mycol = mydb["users"]  # collection_name


MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
client = MongoClient(MONGO_DB_URL)
mydb = client["user_db"]  # database_name
mycol = mydb["users"]  # collection_name

# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
PORT = sys.argv[1]
#PORT = 8080

app = Flask(__name__)
# app.config.update(SESSION_COOKIE_NAME='session2')
app.config['SECRET_KEY'] = 'secret'
# CORS(app, supports_credentials=True)
# CORS(app)
log = logging.getLogger('demo-logger')
# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
# db_user=client['users']


def create_session(session_data):
    session_inst = client.session_db.session_data
    session_inst.update_one(
        {
            "user": session['user']},
        {"$set": {'user': session['user']}},
        upsert=True
    )


def find_session():
    session_inst = client.session_db.session_data
    if session_inst.count_documents() > 0:
        session['user'] = session_inst.find_one(['user'])
        return True
    else:
        return False


def delete_session(session_data):
    session_inst = client.session_db.session_data
    session_inst.delete_many(
        {"user": session['user']}
    )


@ app.route('/signup', methods=['POST'])
def signup():
    """Function to handle requests to /signup route."""
    if(request.method == 'POST'):
        data = request.form

        user_name = data['username']
        password = data['password']
        role = data['role']
        email = data['email']

        check_user = list(mycol.find(
            {"username": user_name}, {"_id": 0, "username": 1}))

        if(check_user != []):
            flash('User already exists', 'info')
            return redirect(url_for('login'))

        else:
            mycol.insert_one(
                {"username": user_name, "password": password, "role": role, "email": email})
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))


@ app.route('/', methods=['POST', 'GET'])
def login():
    """Function to handle requests to /signin route."""
    if(request.method == 'GET'):
        return render_template('login.html')

    if(request.method == 'POST'):
        data = request.form

        username = data['username']
        password = data['password']

        check_user = list(mycol.find({"username": username}))

        if(check_user != []):
            if(check_user[0]['password'] == password):

                session['user'] = check_user[0]['username']
                create_session(session['user'])
                if (check_user[0]['role'] == "Data Scientist"):
                    flash('Successfully logged in as Data Scientist', 'success')
                    return redirect(url_for('home'))

                elif (check_user[0]['role'] == "Application Developer"):
                    flash('Successfully logged in as Application Developer', 'success')
                    return redirect(url_for('home'))

                elif (check_user[0]['role'] == "Platform Configurer"):
                    flash('Successfully logged in as Platform Configurer', 'success')
                    return redirect(url_for('home'))

                else:
                    flash('Successfully logged in as End User', 'success')
                    return redirect(url_for('home'))

            else:
                flash('Invalid credentials', 'error')
                return redirect(url_for('login'))

        else:
            flash('User does not exist', 'info')
            return redirect(url_for('login'))


@ app.route('/signout', methods=['GET'])
def logout():
    delete_session(session['user'])
    session.pop('user', None)
    flash("You have successfully logged out", "success")
    return render_template("logout.html")


@ app.route('/home', methods=['GET'])
def home():
    if 'user' not in session:
        flash('User not logged in', 'error')
        return redirect(url_for('login'))

    else:
        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        # Fetch
        if(user_role == 'Application Developer'):
            return render_template("home.html", role=user_role)
        elif(user_role == 'Data Scientist'):
            return render_template("home.html", role=user_role)
        elif(user_role == 'Platform Configurer'):
            return render_template("home.html", role=user_role)
        else:
            return render_template("home.html", role=user_role)


""" AI Manager """
@app.route('/model/display', methods=['POST', 'GET'])
def model_display():
    # role_check = list(mycol.find({"username": session['user']}))
    # user_role = role_check[0]['role']

    # url = generate_ai_url(user_role)
    
    # username = {"username": session['user']}
    # model_details = requests.get(url, params=username).content

    url = "http://127.0.0.1:6500/model/display"
    # url = getServiceUrl("ai_manager") + "/model/display"
    
    print(url)

    model_details = requests.get(url).content
    return model_details


@app.route('/model/upload', methods=['POST', 'GET'])
def model_upload():
    if request.method == "GET":
        # username = {"username": session['user']}

        # a = requests.get(url, params=username).content

        # return a
        
        url = "http://127.0.0.1:6500/model/upload"
        # url = getServiceUrl("ai_manager") + "/model/upload"

        print(url)

        model_upload_screen = requests.get(url).content
        return model_upload_screen

    else:
        
        # request.files["file"]

        # files = {"file" : request.files}


        url = "http://127.0.0.1:6500/model/upload"
        # url = getServiceUrl("ai_manager") + "/model/upload"
        
        print(url)
        
        file = request.files['file']

        end_screen = requests.post(url, files={'file': (
            file.filename, file.stream, file.content_type, file.headers)}).content

        return end_screen



""" SC MANAGER"""
@app.route('/sc_type/upload', methods=['POST', 'GET'])
def sc_type_upload():
    if request.method == "GET":
        # url = getServiceUrl("sc_manager") + "/sc_type/upload"
        
        url = "http://127.0.0.1:8101" + "/sc_type/upload"
        print(url)

        model_upload_screen = requests.get(url).content
        return model_upload_screen

    else:
        # url = getServiceUrl("sc_manager") + "/sc_type/upload"
        
        url = "http://127.0.0.1:8101" + "/sc_type/upload"
        print(url)

        file = request.files['file']

        end_screen = requests.post(url, files={'file': (
            file.filename, file.stream, file.content_type, file.headers)}).content

        return end_screen


@app.route('/sc_instance/upload', methods=['POST', 'GET'])
def sc_instance_upload():
    if request.method == "GET":
        # url = getServiceUrl("sc_manager") + "/sc_instance/upload"

        url = "http://127.0.0.1:8101" + "/sc_instance/upload"
        print(url)

        model_upload_screen = requests.get(url).content
        return model_upload_screen

    else:
        # url = getServiceUrl("sc_manager") + "/sc_instance/upload"

        url = "http://127.0.0.1:8101" + "/sc_instance/upload"
        print(url)

        file = request.files['file']

        end_screen = requests.post(url, files={'file': (
            file.filename, file.stream, file.content_type, file.headers)}).content

        return end_screen


@app.route('/sc_type/display', methods=['POST', 'GET'])
def sc_type_display():
    # url = getServiceUrl("sc_manager") + "/sc_type/display"
    
    url = "http://127.0.0.1:8101" + "/sc_type/display"
    print(url)
    
    sc_type_details = requests.get(url).content
    return sc_type_details


@app.route('/sc_instance/display', methods=['POST', 'GET'])
def sc_instance_display():
    # url = getServiceUrl("sc_manager") + "/sc_instance/display"
    
    url = "http://127.0.0.1:8101" + "/sc_instance/display"
    print(url)
    
    sc_instance_details = requests.get(url).content
    return sc_instance_details



""" APP MANAGER """
@app.route('/app/display', methods=['GET'])
def app_display():
    # url = getServiceUrl("app_manager") + "/app/display"
    
    url = "http://127.0.0.1:8200" + "/app/display"
    print(url)
    
    app_details = requests.get(url).content
    return app_details


@app.route('/app/upload', methods=['POST', 'GET'])
def app_type_upload():
    if request.method == "GET":
        # url = getServiceUrl("app_manager") + "/app/upload"
        
        url = "http://127.0.0.1:8200" + "/app/upload"
        print(url)

        app_upload_screen = requests.get(url).content
        return app_upload_screen

    else:
        # url = getServiceUrl("app_manager") + "/app/upload"
        
        url = "http://127.0.0.1:8200" + "/app/upload"
        print(url)

        file = request.files['file']

        end_screen = requests.post(url, files={'file': (
            file.filename, file.stream, file.content_type, file.headers)}).content

        return end_screen


@app.route('/app/sc_display', methods=['GET'])
def app_sc_display():
    # url = getServiceUrl("app_manager") + "/app/sc_display"
    
    url = "http://127.0.0.1:8200" + "/app/sc_display"
    print(url)
    
    sc_details = requests.get(url).content
    return sc_details


@app.route('/app/models_display', methods=['GET'])
def app_models_display():
    # url = getServiceUrl("app_manager") + "/app/models_display"
    
    url = "http://127.0.0.1:8200" + "/app/models_display"
    print(url)
    
    model_details = requests.get(url).content
    return model_details



"""END USER"""
@app.route('/end_app/display', methods=['GET'])
def end_app_display():
    url = "http://127.0.0.1:8200/app/return_list"
    
    print(url)
    app_details = requests.get(url).json()["list"]
    print(app_details)

    choice = "app_display"
    
    return render_template("endhome.html", choice=choice, tasks=app_details)


@app.route('/app/deploy', methods=['GET', 'POST'])
def app_dep_config():
    if request.method == "GET":    
        app_id = request.args.get('appid')

        # url = getServiceUrl("app_manager") + "/app/deploy"
        
        url = "http://127.0.0.1:8200" + "/app/deploy"
        print(url)

        data = {"appid": app_id}

        app_upload_screen = requests.get(url, params=data).content

        return app_upload_screen

    else:
        # url = getServiceUrl("app_manager") + "/app/deploy"
        
        url = "http://127.0.0.1:8200" + "/app/deploy"
        print(url)
        
        data = dict(request.form)
        status = requests.post(url, data=data).content

        status = int(status)

        if (status == 1):
            flash("Application config successfully binded and stored.", "success")
            return redirect(url_for('app_instance_display'))

        elif (status == 0):
            flash("Sensors / controllers not present in this location.", "error")
            return redirect(url_for('app_instance_display'))  

        else:
            flash("Invalid application details.", "error")
            return redirect(url_for('app_instance_display'))


# @app.route('/schedule/display', methods=['GET'])
# def schedule_display():
#     try:
#         app_list = []
#         for app_record in client.scheduler.config.find():
#             display_record = {
#                 "app_id": app_record["app_id"],
#                 "app_instance_id": app_record["app_instance_id"],
#                 "start_time": app_record["start_time"],
#                 "end_time": app_record["end_time"],
#                 "periodicity": app_record["periodicity"],
#                 "burst_time": app_record["burst_time"],
#                 "periodicity_unit": app_record["periodicity_unit"],

#             }
#             app_list.append(display_record)
#             log.info(app_list)

#         print(app_list)

#         choice = "schedule_display"
#         return render_template("endhome.html", choice = choice, tasks=app_list)
#         #return render_template('scheduling_display.html', tasks=app_list, role=user_role, url=url)

#     except Exception as e:
#         print("hello2")
#         log.error({'error': str(e)})
#         return redirect(request.url)


@app.route('/app_instance/display', methods=['GET'])
def app_instance_display():
    try:
        app_instance_list = []

        username = session['user']
        for app_instance_record in client.app_db.instance.find({"end_user": username}):

            db = client.node_manager_db
            app = db.app_deployment_metadata.find_one(
                {"app_instance_id": app_instance_record["app_instance_id"]})
            if app == None:
                status = "Pending"
            else:
                status = app["status"]
            display_record = {
                "app_id": app_instance_record["app_id"],
                "app_instance_id": app_instance_record["app_instance_id"],
                "end_user": app_instance_record["end_user"],
                "sensors": app_instance_record["sensors"],
                "controllers": app_instance_record["controllers"],
                "models": app_instance_record["models"],
                "status": status
            }
            app_instance_list.append(display_record)
            log.info(app_instance_list)

        
        choice = "app_instance_display"
        return render_template("endhome.html", choice = choice, tasks=app_instance_list)

    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


@app.route('/app/show_details', methods=['POST'])
def link_redirect():
    if(request.method == 'POST'):
        try:
            app_instance_id = request.form["appinstanceid"]

            db = client.node_manager_db
            app = db.app_deployment_metadata.find_one(
                {"app_instance_id": app_instance_id})

            url = "http://"
            ip = app["ip"]
            port = app["port"]
            d_url = url + ip + ":" + port

            d_url += "/show_details"

            a = requests.get(d_url).content

            return a

        except:
            flash("App Instance Not Live", "error")
            return redirect(url_for('app_instance_display'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)

    # app.run(port=PORT, debug=True, use_debugger=False,
    #        use_reloader=False, passthrough_errors=True)
