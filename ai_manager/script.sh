#!/bin/bash

kill -9 $(ps aux|grep '[p]ython3 server.py' | awk ' { print $2 } ')
python3 server.py $1 &
