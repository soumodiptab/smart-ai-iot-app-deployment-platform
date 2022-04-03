### Files
model.py ---> for training the model and saving the model in a pickle file

preprocess.py ---> Preprocessing of the user inputs wil be done here in a function. This will be imported in the server.py file

server.py ---> model loaded from the pickle file and hosted through rest api

client.py ---> user will send a request to the rest api endpoint along with the input and will receive the output on cli

aiManager.py ---> AI Manager unzips, validates files from Data Scientist and create server.py

dataScientist.py ---> uploads necessary files through zip.

### Running instructions

##### In present Directory
###### python aiManager.py
###### python dataScientist.py

###### cd .\dir\dataScFiles\
###### python server.py

###### cd ..
###### cd ..
##### In present Directory
##### python client.py
