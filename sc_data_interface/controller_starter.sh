#!/bin/bash
python3 start_light.py 127.0.0.1 9003 &
python3 start_display.py 127.0.0.1 9004 &
python3 start_fan.py 127.0.0.1 9005 &
python3 start_computer.py 127.0.0.1 9006 &
python3 start_sprinkler.py 127.0.0.1 9007 &
#------------------------------------------------
# python3 test.py 127.0.0.1 9003
# python3 test.py 127.0.0.1 9004
# python3 test.py 127.0.0.1 9005
# python3 test.py 127.0.0.1 9006
# python3 test.py 127.0.0.1 9007
echo "----------------------------------------------------------"
echo All controllers have been started
echo "----------------------------------------------------------"