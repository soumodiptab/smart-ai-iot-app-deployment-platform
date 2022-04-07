import json
from re import L
import sys
# path1=sys.argv[1]

def generateServer(path):
    fname = path+'/server.py'
    f = open(path+"/config.json")
    config = json.load(f)
    model_file_ext=config["prediction"]["model_type"]
    inp_param_dict=config["preprocessing"]['input_params'][0]
    input_param_type=list(inp_param_dict.items())[0][1]
    wdata=""
    wdata += "from flask import Flask, request, jsonify\n\n"
    wdata += "import sys\n\n"
    if(model_file_ext=="pkl"):
        wdata += "import pickle\n\n"
    elif(model_file_ext=="h5"):
        wdata+= "from tensorflow import keras\n\nfrom uuid import uuid4\n"
    wdata += "import json\nimport os\n\n"
    pre_pr_name=config["preprocessing"]
    wdata+="from "+pre_pr_name["name"][:-3]+" import "+pre_pr_name["method_name"]+"\n"
    post_pr_name=config["postprocessing"]
    wdata+="from "+post_pr_name["name"][:-3]+" import "+post_pr_name["method_name"]+"\n"


    wdata += "portId = "
    wdata += "sys.argv[1]\n\n"


    wdata += "app = Flask(__name__)\n\n"


    wdata += "@app.route('/predict/<modelId>', methods=['POST'])\n\n"
    wdata += "def predict(modelId):\n\t"

    img_extension_list=['jpg','jpeg','png','bmp']
    if (input_param_type in img_extension_list):
        wdata += "data = request.files['image'].read()\n\t"
        wdata +="img_name=uuid4().hex+'."+input_param_type+"'\n\t"
        wdata +="decodeit = open(f'{img_name}', 'wb')\n\t"
        wdata+="decodeit.write(data)\n\t"
        wdata+="decodeit.close( )\n\t"
    else:
        wdata += "data = request.json\n\t"
        # preprocess_frame="l = ["
        # for param in inp_param_dict:
        #     wdata+=param
        #     preprocess_frame+=param+","
        #     wdata+=" = data['"
        #     wdata+=param
        #     wdata+="']\n\t"
        # preprocess_frame=preprocess_frame[:-1]
        # preprocess_frame += "]\n\t"
        # wdata+=preprocess_frame
    wdata += "preprocessed = "
    wdata += pre_pr_name["method_name"]
    if(input_param_type in img_extension_list):
        wdata += "(img_name)\n\t"
        wdata += "os.remove(f'{img_name}')\n\t"
    else:    
        wdata += "(data)\n\t"

    wdata += "filename = '"
    model_file_name = config["prediction"]["name"]
    wdata += model_file_name + "'\n\t"

    wdata += "loaded_model = "
    if(model_file_ext=="pkl"):
        wdata += "pickle.load(open(filename, 'rb'))\n\t"
    elif(model_file_ext=="h5"):
        wdata+= "keras.models.load_model(filename)\n\t"

    wdata += "pred = loaded_model.predict(preprocessed)\n\t"
    wdata += "out="
    wdata +=post_pr_name["method_name"]+"(pred)\n\t"

    wdata += "output = {'output': out}\n\t"

    wdata += "return jsonify(output)\n\n"


    wdata += "if __name__ == '__main__':\n\t"

    wdata += "app.run(host='0.0.0.0', port = portId, debug = False)\n"


    with open(fname, 'w') as f:
        f.write('{}'.format(wdata))

def generateDockerFile(path):
    fname = path + '/Dockerfile'
    wdata = "FROM python:3.8-slim-buster\n\n"
    wdata += "WORKDIR /app\n\n"
    wdata += "COPY requirements.txt requirements.txt\n\n"
    wdata += "RUN pip3 install -r requirements.txt\n\n"
    wdata += "COPY . .\n\n"
    wdata += "ENTRYPOINT [ \"python3\" ]\n\n"
    wdata += "CMD [\"server.py\"]\n\n"
    with open(fname, 'w') as f:
        f.write('{}'.format(wdata))

# generateServer(path1)