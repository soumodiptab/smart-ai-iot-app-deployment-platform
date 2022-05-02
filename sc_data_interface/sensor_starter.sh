#!/bin/bash
pkill -f 'start_'
# python3 start_temp.py 127.0.0.1 7001 25 &
# python3 start_pressure.py 127.0.0.1 7002 35 &
python3 start_image.py 127.0.0.1 7003 images/gun_detection &
python3 start_burst_image.py 127.0.0.1 7004 images/signatures &
echo "----------------------------------------------------------"

python3 test.py 127.0.0.1 7003
python3 test.py 127.0.0.1 7004
echo "----------------------------------------------------------"
echo All sensors have been started
echo "----------------------------------------------------------"