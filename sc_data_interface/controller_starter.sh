#!/bin/bash
python3 start_display.py 127.0.0.1 7021 &
python3 start_buzzer.py 127.0.0.1 7022 &
python3 start_display.py 127.0.0.1 7023 &
python3 start_buzzer.py 127.0.0.1 7024 &