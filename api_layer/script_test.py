import time
from platform_sdk import get_sensor_data, get_sensor_image, send_controller_data
while True:
    print('Waiting...')
    data = get_sensor_data(0)
    print(data)
    print("-------------------------")
    data_set = data*100
    send_controller_data(0, data_set)
    time.sleep(1)
