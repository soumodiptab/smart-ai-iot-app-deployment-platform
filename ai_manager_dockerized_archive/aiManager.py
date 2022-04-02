from flask import Flask, request
from zipfile import ZipFile
import json
import os
import sys
import subprocess
import time

# sys.path.insert(0, "./dir/dataScFiles")
# sys.path.append('./dir/dataScFiles')

app = Flask(__name__)

@app.route('/getResult', methods=['POST'])
def getResult():
    file = request.files['file']
    print (file.filename)
    # relativePath = request.data
    # path = relativePath['rePath']
    # fileAbsolutePath = path + file.filename

    # Unzip stage
    with ZipFile(file.filename, 'r') as f:
        #extract in current directory
        f.extractall('./dir')
    # with ZipFile(fileAbsolutePath, 'r') as f:
    #     #extract in current directory
    #     f.extractall('./dir')
    
    # Validation stage
    f = open("./dir/dataScFiles/config.json")
    config = json.load(f)
    retStatement = ""
    if "name" in config and "description" in config and "readme" in config and "preprocessing" in config and "prediction" in config and "dependency" in config :
        readmeFile = config["readme"]
        preprocessingFile = config["preprocessing"]["name"]
        predictionFile = config["prediction"]["name"]
        dependencyFile = config["dependency"]

        # print(readmeFile + " " + preprocessingFile + " " + predictionFile + " " + dependencyFile)
        
        readmeFileExists = os.path.exists('./dir/./dataScFiles/' + readmeFile)
        preprocessingFileExists = os.path.exists('./dir/./dataScFiles/' + preprocessingFile)
        predictionFileExists = os.path.exists('./dir/./dataScFiles/' + predictionFile)
        dependencyFileExists = os.path.exists('./dir/./dataScFiles/' + dependencyFile)

        if(readmeFileExists and preprocessingFileExists and predictionFileExists and dependencyFileExists):
            print("model, preprocessing, config, readme, requirements file present in ZIP. Verified!!")
            retStatement += "[AI Manager]: model, preprocessing, config, readme, requirements file present in ZIP. Verified!!"

        # print("Key exist in JSON data")
        # print(student["name"], "marks is: ", student["percentage"])
        
        # Generate server.py
        # exec(open("./generate.py").read())
        os.system(f'python3 ./generate.py &')

        # Give some time to generate server.py via generate.py
        time.sleep(3)

        # Run server.py
        # exec(open("./dir/dataScFiles/server.py").read())
        # subprocess.call("./dir/dataScFiles/server.py", shell=True)
        os.system(f'python3 ./dir/dataScFiles/server.py &')

    else:
        print("!!ZIp does not contain all the necessary files to run. Aborting!!")
        retStatement += "[AI Manager]: !!ZIp does not contain all the necessary files to run. Aborting!!"
    return retStatement

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=False)
