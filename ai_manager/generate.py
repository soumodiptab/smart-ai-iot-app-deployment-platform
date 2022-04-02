import json
import sys

def generateServer(path):
    fname = path + '/server.py'
    f = open(path + "/config.json")
    config = json.load(f)
    model_file_ext=config["prediction"]["model_type"]
    wdata=""
    wdata += "from flask import Flask, request, jsonify\n\n"
    wdata += "import sys\n\n"
    # wdata += "import numpy as np\n\n"
    # wdata += "import pandas as pd\n\n" 
    if(model_file_ext=="pkl"):
        wdata += "import pickle\n\n"
    elif(model_file_ext=="h5"):
        wdata+= "from tensorflow import keras\n\n"
    wdata += "import json\n\n"
    wdata += "from pymongo import MongoClient\n\n"
    pre_pr_name=config["preprocessing"]
    wdata+="from "+pre_pr_name["name"][:-3]+" import "+pre_pr_name["method_name"]+"\n"
    post_pr_name=config["postprocessing"]
    wdata+="from "+post_pr_name["name"][:-3]+" import "+post_pr_name["method_name"]+"\n"
    wdata += "import uuid\n\n"

    wdata += "# client=MongoClient()\n\n"
    wdata += "# client = MongoClient(\"mongodb://localhost:27017/\")\n\n"

    wdata += "MONGO_DB_URL = json_config_loader('config/db.json')['ip_port']\n\n"
    wdata += "client = MongoClient(MONGO_DB_URL)\n\n"

    wdata += "modelId = uuid.uuid4().hex\n\n"
    wdata += "portId = "
    wdata += "sys.argv[1]\n\n"


    wdata += "app = Flask(__name__)\n\n"

    # wdata += "def preprocess(l):\n"
    # wdata += "\tl[0] = np.sqrt(l[0])\n"
    # wdata += "\treturn l\n\n"


    wdata += "@app.route('/predict/<modelId>', methods=['POST'])\n\n"
    wdata += "def predict(modelId):\n\t"

    wdata += "data = request.json\n\t"



    inp_param_dict=config["preprocessing"]['input_params'][0]

    preprocess_frame="l = ["
    for param in inp_param_dict:
        wdata+=param
        preprocess_frame+=param+","
        wdata+=" = data['"
        wdata+=param
        wdata+="']\n\t"
    preprocess_frame=preprocess_frame[:-1]
    preprocess_frame += "]\n\t"
    wdata+=preprocess_frame

    wdata += "l = "
    wdata += pre_pr_name["method_name"]
    wdata += "(l)\n\t"

    wdata += "filename = './dir/dataScFiles/"
    model_file_name = config["prediction"]["name"]
    wdata += model_file_name + "'\n\t"

    wdata += "loaded_model = "
    if(model_file_ext=="pkl"):
        wdata += "pickle.load(open(filename, 'rb'))\n\t"
    elif(model_file_ext=="h5"):
        wdata+= "keras.models.load_model(filename)\n\t"

    wdata += "pred = loaded_model.predict(l)\n\t"#???
    # wdata += "x=pred[0]\n\t"
    wdata += "out="
    wdata +=post_pr_name["method_name"]+"(pred)\n\t"

    wdata += "output = {'output': out}\n\t"

    wdata += "return jsonify(output)\n\n"



    wdata += "@app.route('/getModelInfo', methods=['GET'])\n\n"
    wdata += "def getModelInfo():\n\t"


    wdata += "deployedIp = 'http://127.0.0.1'\n\t"
    wdata += "port = portId\n\t"

    wdata += "deployedAddress = deployedIp + ':' + str(port)\n\t"
    wdata += "modelName = 'model1'\n\t"

    wdata += "db = client[\"ai_data\"]\n\t"
    wdata += "my_collection = db[\"model_info\"]\n\t"
    wdata += "config = json.load(open(\"./dir/dataScFiles/config.json\"))\n\t"

    wdata += "data = {'deployedAddress': deployedAddress, 'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp, 'port': port, 'config': config}\n\t"

    wdata += "data1 = {'deployedAddress': deployedAddress, 'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp, 'port': port, 'config': config}\n\t"

    wdata += "# my_collection.insert_one(data1)\n\t"

    wdata += "return data\n\n"


    wdata += "if __name__ == '__main__':\n\t"

    wdata += "app.run(port = portId, debug = False)\n"


    with open(fname, 'w') as f:
        f.write('{}'.format(wdata))