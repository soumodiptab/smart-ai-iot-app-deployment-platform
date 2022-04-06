from crontab import CronTab
import configparser


config = configparser.ConfigParser()
with open('scheduler_config.ini', 'w') as configfile:
    config.write(configfile)

def addToCron(data):
    app_id = data["app_id"]
    app_instance_id = data["app_instance_id"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    periodicity = data["periodicity"]
    periodicity_unit = data["periodicity_unit"]
    is_model = data["is_model"]

    my_cron = CronTab(user=config["cron"]["user"])

    job = my_cron.new(command='python3 /home/vishal/Documents/sem2/IAS/smart-ai-iot-app-deployment-platform/app_start.py ' + app_id + " " + app_instance_id + " " + is_model)

    start_time = start_time.split(":")

    job.minute.on(start_time[1])
    job.hour.on(start_time[0])

    job1 = my_cron.new(command='python3 /home/vishal/Documents/sem2/IAS/smart-ai-iot-app-deployment-platform/node_manager/app_start.py ' + app_id + " " + app_instance_id + 
        + " " + is_model)

    if periodicity:
        if periodicity_unit == "Mins":
            job1.every(periodicity).min()

        if periodicity_unit == "Hrs":
            job1.every(periodicity).hour()

    end_time = end_time.split(":")
    job2 = my_cron.new(command='python3 /home/vishal/Documents/sem2/IAS/smart-ai-iot-app-deployment-platform/node_manager/app_stop.py ' + app_id + " " + app_instance_id)
    job2.minute.on(end_time[1])
    job2.hour.on(end_time[0])

    my_cron.write()