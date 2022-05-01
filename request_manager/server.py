from flask import Flask, render_template, session, request, redirect, url_for, flash
import sys
from pymongo import MongoClient
from utils import json_config_loader
from platform_logger import get_logger
import requests

INITIALIZER_ADDRESS = json_config_loader('config/initialiser.json')["ADDRESS"]
KAFKA_SERVERS = json_config_loader('config/kafka.json')["bootstrap_servers"]
log = get_logger('request_manager', KAFKA_SERVERS)


def getServiceUrl(service_name):
    URL = "http://" + INITIALIZER_ADDRESS + \
        "/initialiser/getService/" + service_name
    r = requests.get(url=URL)
    data = r.json()
    ip = data["ip"]
    port = data["port"]
    url = "http://" + ip + ":" + port
    return url


MONGO_DB_URL = json_config_loader('config/db.json')['DATABASE_URI']
client = MongoClient(MONGO_DB_URL)
mydb = client["user_db"]  # database_name
mycol = mydb["users"]  # collection_name

# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
PORT = sys.argv[1]
# PORT = 8080

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
# MONGO_DB_URL = "mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
# db_user=client['users']


@app.route('/signup', methods=['POST'])
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
                {"username": user_name, "password": password, "name": role, "email": email})
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
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


@app.route('/signout', methods=['GET'])
def logout():
    session.pop('user', None)
    flash("You have successfully logged out", "success")

    return render_template("logout.html")


@app.route('/home', methods=['GET'])
def home():
    if 'user' not in session:
        flash('User not logged in', 'error')
        return redirect(url_for('login'))

    else:
        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']
        db = client.initialiser_db
        ai_ip = db.ips.find_one({"name": "ai_manager"})
        app_ip = db.ips.find_one({"name": "app_manager"})
        sc_ip = db.ips.find_one({"name": "sc_manager"})
        request_ip = db.ips.find_one({"name": "request"})
        url = "http://"
        url2 = "http://"
        url3 = "http://"
        # Fetch
        if(user_role == 'Application Developer'):
            ip = app_ip["ip"]
            port = app_ip["port"]
            url = url + ip + ":" + port
            ip = sc_ip["ip"]
            port = sc_ip["port"]
            url2 = url2 + ip + ":" + port
            ip = ai_ip["ip"]
            port = ai_ip["port"]
            url3 = url3 + ip + ":" + port
        elif(user_role == 'Data Scientist'):
            return render_template("home.html", role=user_role)
        elif(user_role == 'Platform Configurer'):
            ip = sc_ip["ip"]
            port = sc_ip["port"]
            url = url + ip + ":" + port
        else:
            ip = app_ip["ip"]
            port = app_ip["port"]
            url = url + ip + ":" + port
        return render_template("home.html", role=user_role, url=url, url2=url2, url3=url3)


@app.route('/schedule/display', methods=['GET'])
def schedule_display():
    try:

        app_list = []
        for app_record in client.scheduler.config.find():
            display_record = {
                "app_id": app_record["app_id"],
                "app_instance_id": app_record["app_instance_id"],
                "start_time": app_record["start_time"],
                "end_time": app_record["end_time"],
                "periodicity": app_record["periodicity"],
                "burst_time": app_record["burst_time"],
                "periodicity_unit": app_record["periodicity_unit"],

            }
            app_list.append(display_record)
            log.info(app_list)

        role_check = list(mycol.find({"username": session['user']}))
        user_role = role_check[0]['role']

        db = client.initialiser_db
        request_ip = db.ips.find_one({"name": "request"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        url = url + ip + ":" + port

        print("hello1")
        return render_template('scheduling_display.html', tasks=app_list, role=user_role, url=url)

    except Exception as e:
        print("hello2")
        log.error({'error': str(e)})
        return redirect(request.url)


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

        db = client.initialiser_db
        request_ip = db.ips.find_one({"name": "request"})
        # print(request_ip)
        url = "http://"
        ip = request_ip["ip"]
        port = request_ip["port"]
        url = url + ip + ":" + port

        return render_template('app_instances.html', tasks=app_instance_list, url=url)

    except Exception as e:
        log.error({'error': str(e)})
        return redirect(request.url)


@app.route('/app/show_details', methods=['POST'])
def link_redirect():
    if(request.method == 'POST'):
        try:
            app_instance_id = request.form["appinstanceid"]

            db = client.node_manager_db
            # app = db.app_deployment_metadata.find_one(
            #     {"app_instance_id": app_instance_id})

            # url = "http://"""
            # ip = app["ip"]
            # port = app["port"]
            # d_url = url + ip + ":" + port
            # d_url += "/show_details"
            node_url = getServiceUrl('node_manager')
            #a = requests.get(d_url).content
            #return a
            return "fakelink"
        except:
            flash("App Instance Not Live", "error")
            return redirect(url_for('app_instance_display'))


""" AI Manager """


@app.route('/model/display', methods=['POST', 'GET'])
def model_display():
    # role_check = list(mycol.find({"username": session['user']}))
    # user_role = role_check[0]['role']

    # url = generate_ai_url(user_role)
    # url = "http://127.0.0.1:6500/model/display"

    # username = {"username": session['user']}
    # model_details = requests.get(url, params=username).content

    url = getServiceUrl("ai_manager") + "/model/display"
    print(url)

    model_details = requests.get(url).content
    return model_details


@app.route('/model/upload', methods=['POST', 'GET'])
def model_upload():
    if request.method == "GET":
        # url = "http://127.0.0.1:6500/model/upload"

        # username = {"username": session['user']}

        # a = requests.get(url, params=username).content

        # return a
        url = getServiceUrl("ai_manager") + "/model/upload"
        print(url)

        model_upload_screen = requests.get(url).content
        return model_upload_screen

    else:
        url = getServiceUrl("ai_manager") + "/model/upload"

        # request.files["file"]

        # files = {"file" : request.files}

        file = request.files['file']

        end_screen = requests.post(url, files={'file': (
            file.filename, file.stream, file.content_type, file.headers)}).content

        return end_screen
        return "upload button pressed"


@app.route('/notif', methods=['GET'])
def notif():
    return "Notifications will be done one day..... hopefully!!!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)

    # app.run(port=PORT, debug=True, use_debugger=False,
    #        use_reloader=False, passthrough_errors=True)
