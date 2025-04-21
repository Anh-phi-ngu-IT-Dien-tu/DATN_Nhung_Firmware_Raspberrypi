from robot_mqtt import Robot_MQTT_Position 
import os
import shutil
import time
import json
from datetime import datetime

path="./shelves_information_report"

gui=Robot_MQTT_Position(host="broker.emqx.io",topic="GUI",use_coordinate=False)
gui.start_mqtt()

message=''

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            full_path = os.path.join(root, file)
            with open(full_path,"r") as readfile:
                data = json.load(readfile)
            message=message+f'{file} result: {data}\n'

now=datetime.now()
day=now.day
month=now.month
year=now.year
hour=now.hour
minute=now.minute
second=now.second
message=message+f"date: {day}/{month}/{year} time: {hour}:{minute}:{second} \n"
gui.publish(gui.topic,message)
time.sleep(5)
gui.stop_mqtt()