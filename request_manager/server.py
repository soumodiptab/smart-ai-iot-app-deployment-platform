from flask import Flask, render_template, session, request, redirect, url_for, flash
import pymongo

from logging import Logger
import logging
import sys
from pymongo import MongoClient
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["user_db"]  # database_name
mycol = mydb["users"]  # collection_name

#PORT = sys.argv[1]
PORT = 8080

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

log = logging.getLogger('demo-logger')
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
        email =data['email']

        check_user = list(mycol.find(
            {"username": user_name}, {"_id": 0, "username": 1}))

        if(check_user != []):
            flash('User already exists', 'info')
            return redirect(url_for('login'))

        else:
            mycol.insert_one(
                {"username": user_name, "password": password, "role": role,"email":email})
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
        role_check=list(mycol.find({"username": session['user']}))
        user_role=role_check[0]['role']
        url = "http://"
        # Fetch 
        if(user_role=='Application Developer'):
            ip = "127.0.0.1"
            port = "8200"
            url=url+ ip + ":" + port
        elif(user_role=='Data Scientist'):
            ip = "127.0.0.1"
            port = "6500"
            url=url+ ip + ":" + port 
        elif(user_role=='Platform Configurer'):
            ip = "127.0.0.1"
            port = "8101"
            url=url+ ip + ":" + port 
        else:
            ip = "127.0.0.1"
            port = "8200"
            url=url+ ip + ":" + port
        
        return render_template("home.html", role=user_role, url=url)


@app.route('/schedule/display', methods=['GET'])
def schedule_display():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
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

        role_check=list(mycol.find({"username": session['user']}))
        user_role=role_check[0]['role']

        url = "http://"
        ip = "127.0.0.1"
        port = "8200"
        url=url+ ip + ":" + port
        
        print("hello1")
        return render_template('scheduling_display.html', tasks=app_list, role=user_role, url=url)
        
    except Exception as e:
        print("hello2")
        log.error({'error': str(e)})
        return redirect(request.url)

@app.route('/app_instance/display', methods=['GET'])
def app_instance_display():
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        app_instance_list = []

        username = session['user']
        for app_instance_record in client.app_db.instance.find({"end_user": username}):
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
    # app.run(host="0.0.0.0",port=PORT, debug=True, use_debugger=False,
    #         use_reloader=False, passthrough_errors=True)
    
    app.run(port=PORT, debug=True, use_debugger=False,
            use_reloader=False, passthrough_errors=True)
