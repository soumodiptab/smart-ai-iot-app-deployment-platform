#!/bin/bash
pkill -f 'start_'
# python3 start_temp.py 127.0.0.1 7001 25 &
# python3 start_pressure.py 127.0.0.1 7002 35 &
python3 start_image.py 127.0.0.1 7003 images/celebrity &
python3 start_burst_image.py 127.0.0.1 7004 images/motion &
python3 start_temp.py 127.0.0.1 7005 56 &
python3 start_temp.py 127.0.0.1 7006 56 &
python3 start_temp.py 127.0.0.1 7007 56 &
# python3 start_burst_image.py 127.0.0.1 7004 images/signatures &
echo "----------------------------------------------------------"
# python3 test.py 127.0.0.1 7003
# python3 test.py 127.0.0.1 7004
# python3 test.py 127.0.0.1 7005
# python3 test.py 127.0.0.1 7006
# python3 test.py 127.0.0.1 7007
echo "----------------------------------------------------------"
echo All sensors have been started
echo "----------------------------------------------------------"
