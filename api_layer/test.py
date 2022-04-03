from platform_sdk import get_sensor_data, send_controller_data, get_sensor_image
import time
print('App init....')
while True:
    try:
        data = get_sensor_image(0)
        decodeit = open(f'img_stat.png', 'wb')
        decodeit.write(data)
        decodeit.close()
        print('SENSORS:')
        print(f"::: {data} :::")
        print('Controller:')
        new_data = data*10
        print(f"::: {new_data} :::")
        send_controller_data(0)
        time.sleep(1)
    except KeyboardInterrupt:
        print('Exiting...')
