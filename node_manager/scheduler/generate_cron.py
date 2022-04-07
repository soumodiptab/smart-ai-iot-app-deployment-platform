from crontab import CronTab
import yaml
import os

config_file = os.environ.get("SCHEDULER_HOME") + "/config.yml"
with open(config_file, "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

def addToCron(data):
    print(data)
    if "app_instance_id" not in data:
        return
    app_id = data["app_id"]
    app_instance_id = data["app_instance_id"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    periodicity = data["periodicity"]
    periodicity_unit = data["periodicity_unit"]

    if data["isModel"]:
        is_model = str(1)
    else:
        is_model = str(0)


    my_cron = CronTab(user=cfg["cron"]["user"])

    home_directory = os.environ.get("NODE_AGENT_HOME")
    app_cron_dir = os.environ.get("APP_CRON_HOME")

    start_script = app_cron_dir + "/app_start.py"

    job = my_cron.new(command='/usr/bin/python3 ' + start_script + " " + app_id + " " + app_instance_id + " " + is_model+ " " + periodicity + " " + periodicity_unit)

    start_time = start_time.split(":")

    job.minute.on(start_time[1])
    job.hour.on(start_time[0])


    end_time = end_time.split(":")

    stop_script = app_cron_dir + "/app_stop.py"
    job2 = my_cron.new(command='/usr/bin/python3 ' + stop_script + " " + app_id + " " + app_instance_id)
    job2.minute.on(end_time[1])
    job2.hour.on(end_time[0])

    my_cron.write()
    print("cron written")


data = {
"app_id": "cad8951105d74f3bbfd57c33fd518c31",
"app_instance_id": "cad8951105d74f3bbfd57c33fd518c31",
"instances_count": 2,
"geo_loc": {
    "street": "RANDOM",
    "city": "HYD"
},
"start_time": "16:35",
"end_time": "18:36",
"periodicity": "2",
"periodicity_unit": "Hrs",
"isModel":"False"
}
addToCron(data)