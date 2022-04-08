#!/bin/bash

# Stop All Docker Containers
sudo docker kill $(docker ps -q)

# Remove all exited docker containers
docker rm $(docker ps --filter status=exited -q)

# Print Docker status
sudo docker ps
