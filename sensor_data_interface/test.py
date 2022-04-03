import sensor_data_interface.interfaces as interfaces
import time
# temp_sensor = TEMP("127.0.0.1", "9061", {"street": "RANDOM", "city": "HYD"})
type = 'IMAGE'
geo_loc = str({"street": "RANDOM", "city": "HYD"})
ip_port = '127.0.0.1:9008'
latency = 13
expression = 'sensor_interface.'+type + '('+'\"'+ip_port+'\"'+','+str(latency)+')'
image_sensor = eval(expression)
image_sensor.set_data_source('images/gun_detection')
image_sensor.start()
# time.sleep(10)
# image_sensor.stop()
