from scripts.script1 import script_function
from ipaddress import ip_address
import threading
from flask import Flask, render_template, request, jsonify
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient
import logging
from platform_sdk import get_mongo_db_uri
app = Flask(__name__)
app.secret_key = "secret key"


@app.route('/app/stats', methods=['GET'])
def app_stat_config():
    if request.method == "GET":
        try:
            MONGO_DB_URL = get_mongo_db_uri()
            client = MongoClient(MONGO_DB_URL)
            db = client.model_stat
            Project_List_Col = db.instance
            model_record = Project_List_Col.find_one({"modelId": "0"})
            count0 = model_record['class_0']
            count1 = model_record['class_1']
            count2 = model_record['class_2']
            count3 = model_record['class_3']
            count4 = model_record['class_4']
            return render_template('simple.html', count0=count0, count1=count1, count2=count2, count3=count3, count4=count4)
        except Exception as e:
            return redirect(request.url)


@app.route('/show_details', methods=['GET', 'POST'])
def model_display():
    try:
        MONGO_DB_URL = get_mongo_db_uri()
        client = MongoClient(MONGO_DB_URL)
        ai_model_list = []
        display_record = {
            "modelId": 0,
            "modelName": "weather system",
        }
        ai_model_list.append(display_record)
        return render_template('display.html', tasks=ai_model_list)
    except Exception as e:
        print("exception occurred")


if __name__ == '__main__':
    x = threading.Thread(target=script_function, args=())
    app.run(port=6015, debug=True, use_debugger=False, host='0.0.0.0',
            use_reloader=False, passthrough_errors=True)
