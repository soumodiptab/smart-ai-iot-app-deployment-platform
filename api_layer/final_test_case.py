from platform_sdk import get_stream_image
import time
print('App init....')
counter=0
images = []
while True:
    try:
        counter=0
        data = get_stream_image(0,6)
        for img in data:
            counter=counter+1
            decodeit = open(f'img_stat{counter}.png', 'wb')
            decodeit.write(img)
            decodeit.close()
        print('SENSORS:')
        print(f"::: {data} :::")
        print('Controller:')
        new_data = data*10
        print(f"::: {new_data} :::")
        time.sleep(8)
    except KeyboardInterrupt:
        print('Exiting...')
