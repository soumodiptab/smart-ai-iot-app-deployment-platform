#!/bin/bash

# For Request Manager
cd request_manager
kill -9 $(ps aux|grep '[p]ython3 request_manager/rmServer.py' | awk ' { print $2 } ')
python3 rmServer.py &
cd ..
sleep 1

# For App manager
cd app_manager
kill -9 $(ps aux|grep '[p]ython3 app_manager/appServer.py' | awk ' { print $2 } ')
python3 appServer.py &
cd ..
sleep 1

# Deployer part
cd node_manager
kill -9 $(ps aux|grep '[p]ython3 node_manager/deployer.py' | awk ' { print $2 } ')
python3 deployer.py &
cd ..
sleep 1

cd node_manager
kill -9 $(ps aux|grep '[p]ython3 node_manager/node_manager.py' | awk ' { print $2 } ')
python3 node_manager.py &
cd ..
sleep 1

# cd node_manager
# kill -9 $(ps aux|grep '[p]ython3 node_manager/node_agent.py' | awk ' { print $2 } ')
# python3 node_agent.py &
# cd ..
# sleep 1

# # Ai manager
cd ai_manager
kill -9 $(ps aux|grep '[p]ython3 ai_manager/aiServer.py' | awk ' { print $2 } ')
python3 aiServer.py &
cd ..
sleep 1

# # Sensor manager
cd sc_manager
kill -9 $(ps aux|grep '[p]ython3 sensor_manager/scServer.py' | awk ' { print $2 } ')
python3 scServer.py &
cd ..
sleep 1

# # sensor_data_interface
cd sensor_data_interface
kill -9 $(ps aux|grep '[p]ython3 sensor_data_interface/simulator.py' | awk ' { print $2 } ')
python3 simulator.py &
cd ..
sleep 1

