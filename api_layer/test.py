from platform_sdk import get_sensor_data

print('App init....')
while True:
    temp_data1 = get_sensor_data(1)
    temp_data1 = get_sensor_data(2)
    pres_data = get_sensor_data(3)
    print('SENSORS:')
    print("::: {temp_data1} : {temp_data1} : {pres_data} :::")
    