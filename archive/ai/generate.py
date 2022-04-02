import json
import sys

fname = './dir/dataScFiles/server.py'

wdata = "from flask import Flask, request\n"
wdata += "import numpy as np\n"
wdata += "import pandas as pd\n" 
wdata += "import pickle\n"
wdata += "import json\n"
wdata += "import sys\n"
wdata += "from pymongo import MongoClient\n"
wdata += "import uuid\n"

wdata += "from preprocess import preprocess\n\n"

wdata += "# sys.path.append('./dir/dataScFiles')\n\n"

wdata += "# client = MongoClient('mongodb://localhost:27017/')\n\n"
wdata += "CONNECTION_STRING = 'mongodb+srv://mongo2mongo:test123@cluster0.7ik1k.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'\n"

wdata += "client = MongoClient(CONNECTION_STRING)\n\n"
wdata += "modelId = uuid.uuid4().hex\n\n"
wdata += "portId = 6001\n\n"


wdata += "app = Flask(__name__)\n\n"

wdata += "# def preprocess(l):\n"
wdata += "# \tl[0] = np.sqrt(l[0])\n"
wdata += "# \treturn l\n\n"

wdata += "@app.route('/predict/<modelId>', methods=['POST'])\n\n"
wdata += "def predict(modelId):\n\t"

wdata += "data = request.json\n\t"

wdata += "perc = data['perc']\n\t"
wdata += "temp_max = data['temp_max']\n\t"

wdata += "l = [perc, temp_max]\n\t"

wdata += "l = preprocess(l)\n\t"

# This path is w.r.t to docker directory
wdata += "filename = './dir/dataScFiles/model.pkl'\n\t"
wdata += "loaded_model = pickle.load(open(filename, 'rb'))\n\t"

wdata += "print(len(data))\n\t"

wdata += "pred = loaded_model.predict([l])\n\t"

wdata += "d = {0:'Drizzle', 1:'Fog', 2:'Rain', 3:'Snow', 4:'Sun'}\n\t"

wdata += "return str(d[pred[0]])\n\n"

wdata += "# return str(pred[0])\n\n"


wdata += "@app.route('/getModelInfo', methods=['GET'])\n\n"
wdata += "def getModelInfo():\n\t"


wdata += "deployedIp = 'http://127.0.0.1'\n\t"
wdata += "port = portId\n\t"

wdata += "deployedAddress = deployedIp + ':' + str(port)\n\t"
wdata += "modelName = 'model1'\n\t"

wdata += "db = client[\"ai_data\"]\n\t"
wdata += "my_collection = db[\"model_info\"]\n\t"
# This path is w.r.t to docker directory
wdata += "config = json.load(open(\"./dir/dataScFiles/config.json\"))\n\t"
wdata += "modelName = config['name']\n\t"
wdata += "# print(modelName)\n\t"

wdata += "data = {'deployedAddress': deployedAddress, 'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp, 'port': port, 'config': config}\n\t"
wdata += "data1 = {'deployedAddress': deployedAddress, 'modelId': modelId, 'modelName': modelName, 'deployedIp': deployedIp, 'port': port, 'config': config}\n\t"

wdata += "my_collection.insert_one(data1)\n\t"

wdata += "return data\n\n"


wdata += "if __name__ == '__main__':\n\t"

wdata += "app.run(host='0.0.0.0', port = portId, debug = False)\n"


with open(fname, 'w') as f:
    f.write('{}'.format(wdata))
