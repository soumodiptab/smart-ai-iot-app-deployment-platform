#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
kill -9 $(ps aux|grep '[p]ython3 server.py' | awk ' { print $2 } ')
python3 server.py $1 &
