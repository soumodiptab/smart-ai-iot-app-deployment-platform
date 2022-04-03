from platform_sdk import get_sensor_data, send_controller_data, get_prediction
import time
while True:
    print('--------------------------------------------------------')
    data = get_sensor_data(0)
    print(f"sensor:{data}")
    controller_data = data*1000
    send_controller_data(0, controller_data)
    print('--------------------------------------------------------')
    time.sleep(10)
