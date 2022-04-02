import requests
from zipfile import ZipFile
import os

url = "http://localhost:6000/getResult"

# fileobj = open('test.zip', 'rb')
# # r = requests.post(url, data={"mysubmit":"Go"}, files={"archive": ("test.zip", fileobj)})
# r = requests.post(url, data={"mysubmit":"Go"}, files={"archive": fileobj})

print("**********Select Option**********")
print("1. Upload the preprocessing.py, model.pkl, config.json, requirements.txt as a zip")
print("2. EXIT")
input = int(input("Select option: "))
if(input == 1):
    # create a ZipFile object
    zipObj = ZipFile('AI.zip', 'w')
    # Add multiple files to the zip
    zipObj.write('./dataScFiles/requirements.txt')
    zipObj.write('./dataScFiles/config.json')
    zipObj.write('./dataScFiles/readme.md')
    zipObj.write('./dataScFiles/preprocess.py')
    zipObj.write('./dataScFiles/model.pkl')
    # close the Zip File
    zipObj.close()

    fin = open('AI.zip', 'rb')
    files = {'file': fin}
    r = requests.post(url, files=files)
    # relativePath = {"rePath": "./dataScFiles"}
    # r = requests.post(url, data=relativePath, files=files)
    print (r.text)
    # os.remove("AI.zip")
else:
    exit()



# # create a ZipFile object
# zipObj = ZipFile('AI.zip', 'w')
# # Add multiple files to the zip
# zipObj.write('requirements.txt')
# zipObj.write('config.json')
# # close the Zip File
# zipObj.close()

# fin = open('AI.zip', 'rb')
# files = {'file': fin}
# r = requests.post(url, files=files)
# print (r.text)
