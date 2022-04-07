#!/bin/bash

# Stop All Docker Containers
sudo docker kill $(docker ps -q)

# Print Docker status
sudo docker ps -a
