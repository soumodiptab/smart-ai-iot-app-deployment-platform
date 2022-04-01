from platform_sdk import get_sensor_data, send_controller_data
import time
print('App init....')
while True:
    try:
        data = get_sensor_data(0)
        print('SENSORS:')
        print(f"::: {data} :::")
        print('Controller:')
        new_data = data*10
        print(f"::: {new_data} :::")
        send_controller_data(0)
        time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')
