from platform_sdk import get_sensor_data, send_controller_data, get_prediction
import time
while True:
    print('--------------------------------------------------------')
    data = get_sensor_data(0)
    send_controller_data(0, data)
    print('--------------------------------------------------------')
    time.sleep(10)
