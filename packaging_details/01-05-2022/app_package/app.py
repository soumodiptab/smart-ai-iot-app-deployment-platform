
from ipaddress import ip_address
from flask import Flask, render_template, request, jsonify
from flask import Flask, flash, redirect, render_template, request, jsonify, url_for
from pymongo import MongoClient
import logging
# from platform_sdk import get_mongo_db_uri
app = Flask(__name__)
app.secret_key = "secret key"
log=logging.getLogger('demo-logger')
# MONGO_DB_URL ="mongodb://localhost:27017/"
# client = MongoClient(MONGO_DB_URL)
# db = client.ai_data
# model_info_data = db.model_info
@app.route('/app/stats', methods=['GET'])
def app_stat_config():
    if request.method == "GET":
        try:
            # MONGO_DB_URL = get_mongo_db_uri()
            MONGO_DB_URL ="mongodb://localhost:27017/"
            client = MongoClient(MONGO_DB_URL)
            db = client.model_stat
            Project_List_Col = db.instance

            modelid = request.args.get('modelid')
            # modelid = "6bff908dd35e487b819568fc5deb23c1"
            model_record=Project_List_Col.find( {"modelId" : modelid} )
            
            count0 = model_record[0]['class_0']
            count1 = model_record[0]['class_1']
            count2 = model_record[0]['class_2']
            count3 = model_record[0]['class_3']
            count4 = model_record[0]['class_4']

            # print(count1,"----",count0)
            return render_template('simple.html',count0=count0 ,count1=count1,count2=count2,count3=count3,count4=count4)
            return "0"
        except Exception as e:
            # return "1"
            log.error({'error': str(e)})
            return redirect(request.url)
        
        
   

@app.route('/show_details', methods=['GET','POST'])
def model_display():

    
    try:
        MONGO_DB_URL = "mongodb://localhost:27017/"
        client = MongoClient(MONGO_DB_URL)
        db = client.ai_data
        ai_model_list=[]
        Project_List_Col = db.model_info
        i=0
        for model_record in list(Project_List_Col.find()): 
            display_record={
                "modelId": model_record["modelId"],
                "modelName": model_record["modelName"],
            }
            ai_model_list.append(display_record)
        return render_template('display.html',tasks=ai_model_list)
    except Exception as e:
        log.error({'error': str(e)})


if __name__ == '__main__':
    app.run(port=6015, debug=True, use_debugger=False,host='0.0.0.0',
            use_reloader=False, passthrough_errors=True)
