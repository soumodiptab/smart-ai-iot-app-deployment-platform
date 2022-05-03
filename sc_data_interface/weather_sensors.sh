#!/bin/bash
python3 start_temp.py 127.0.0.1 7001 56 &
python3 start_pressure.py 127.0.0.1 7002 56 &
python3 start_display.py 127.0.0.1 7021 &
python3 test.py 127.0.0.1 7001
python3 test.py 127.0.0.1 7002
python3 test.py 127.0.0.1 7021