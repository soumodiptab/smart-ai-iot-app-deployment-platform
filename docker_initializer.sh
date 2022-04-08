#!/bin/bash

# pull the latest repo
git pull

# Remove all dangling docker images
sudo docker image prune --force

# Docker run for ai_manager
cd ai_manager
sudo docker build -t ai_manager:latest . 
sudo docker run -d -p 6500:6500 ai_manager
# Remove container upon exit
# sudo docker run -d --rm -p 6500:6500 ai_manager
cd ..

# Docker run for app_manager
cd app_manager
sudo docker build -t app_manager:latest . 
sudo docker run -d -p 8200:8200 app_manager
# Remove container upon exit
# sudo docker run -d --rm -p 8200:8200 app_manager
cd ..

# Docker run for request_manager
cd request_manager
sudo docker build -t request_manager:latest . 
sudo docker run -d -p 8080:8080 request_manager
# Remove container upon exit
# sudo docker run -d --rm -p 8080:8080 request_manager
cd ..

# Docker run for sc_manager
cd sc_manager
sudo docker build -t sc_manager:latest . 
sudo docker run -d -p 8101:8101 sc_manager
# Remove container upon exit
# sudo docker run -d --rm -p 8101:8101 sc_manager
cd ..

# Docker run for sensor_data_interface
cd sensor_data_interface
sudo docker build -t simulator:latest . 
sudo docker run -d simulator
# Remove container upon exit
# sudo docker run -d --rm simulator
cd ..

# Docker run for test_model
cd ~/test/model
sudo docker build -t testmodel:latest . 
sudo docker run -d -p 9050:9050 testmodel 9050
# Remove container upon exit
# sudo docker run -d --rm -p 9050:9050 testmodel 9050
cd ~

# Print Docker status
sudo docker ps
