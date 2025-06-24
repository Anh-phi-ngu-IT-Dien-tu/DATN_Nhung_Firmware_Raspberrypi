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

message='stop\n'
            
now=datetime.now()
day=now.day
month=now.month
year=now.year
hour=now.hour
minute=now.minute
second=now.second
message=message+f"date: {day}/{month}/{year} time: {hour}:{minute}:{second} \n"
gui.publish(gui.topic,message)
gui.stop_mqtt()