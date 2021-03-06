#!/bin/bash
if [ ! -f /usr/bin/mongod ]
    then
        sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
        echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
        sudo apt-get update -y
        sudo apt-get install mongodb-org -y
        sudo mkdir -p /data/db
        sudo chown -R $USER /data/db 
        sudo chmod -R go+w /data/db
else
  echo "mongo db already installed.  Skipping..."
fi
mongod

# https://stackoverflow.com/a/56619417