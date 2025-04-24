from robot_mqtt import Robot_MQTT_Position 
import os
import shutil
import time
import json
import ast
from datetime import datetime

path="./shelves_information_report"

gui=Robot_MQTT_Position(host="broker.emqx.io",topic="GUI",use_coordinate=False)
gui.start_mqtt()

with open(path+'/Wrong_object_in_shelf1_1.json',"r") as readfile:
    Shelf1_1wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf1_2.json',"r") as readfile:
    Shelf1_2wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf2_1.json',"r") as readfile:
    Shelf2_1wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf2_2.json',"r") as readfile:
    Shelf2_2wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf3_1.json',"r") as readfile:
    Shelf3_1wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf3_2.json',"r") as readfile:
    Shelf3_2wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf4_1.json',"r") as readfile:
    Shelf4_1wrong_object_data=json.load(readfile)

with open(path+'/Wrong_object_in_shelf4_2.json',"r") as readfile:
    Shelf4_2wrong_object_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf1_1.json',"r") as readfile:
    Shelf1_1soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf1_2.json',"r") as readfile:
    Shelf1_2soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf2_1.json',"r") as readfile:
    Shelf2_1soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf2_2.json',"r") as readfile:
    Shelf2_2soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf3_1.json',"r") as readfile:
    Shelf3_1soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf3_2.json',"r") as readfile:
    Shelf3_2soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf4_1.json',"r") as readfile:
    Shelf4_1soos_data=json.load(readfile)

with open(path+'/Semi_out_of_stock_report_in_shelf4_2.json',"r") as readfile:
    Shelf4_2soos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf1_1.json',"r") as readfile:
    Shelf1_1oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf1_2.json',"r") as readfile:
    Shelf1_2oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf2_1.json',"r") as readfile:
    Shelf2_1oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf2_2.json',"r") as readfile:
    Shelf2_2oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf3_1.json',"r") as readfile:
    Shelf3_1oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf3_2.json',"r") as readfile:
    Shelf3_2oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf4_1.json',"r") as readfile:
    Shelf4_1oos_data=json.load(readfile)

with open(path+'/Out_of_stock_report_in_shelf4_2.json',"r") as readfile:
    Shelf4_2oos_data=json.load(readfile)

message=''

data= f"Shelf1_1/Wrong object :{Shelf1_1wrong_object_data}/-- SOOS:{Shelf1_1soos_data}/-- OOS:{Shelf1_1oos_data}\n"
data2=f"Shelf1_2/Wrong object :{Shelf1_2wrong_object_data}/-- SOOS:{Shelf1_2soos_data}/-- OOS:{Shelf1_2oos_data}\n"
data3=f"Shelf2_1/Wrong object :{Shelf2_1wrong_object_data}/-- SOOS:{Shelf2_1soos_data}/-- OOS:{Shelf2_1oos_data}\n"
data4=f"Shelf2_2/Wrong object :{Shelf2_2wrong_object_data}/-- SOOS:{Shelf2_2soos_data}/-- OOS:{Shelf2_2oos_data}\n"
data5=f"Shelf3_1/Wrong object :{Shelf3_1wrong_object_data}/-- SOOS:{Shelf3_1soos_data}/-- OOS:{Shelf3_1oos_data}\n"
data6=f"Shelf3_2/Wrong object :{Shelf3_2wrong_object_data}/-- SOOS:{Shelf3_2soos_data}/-- OOS:{Shelf3_2oos_data}\n"
data7=f"Shelf4_1/Wrong object :{Shelf4_1wrong_object_data}/-- SOOS:{Shelf4_1soos_data}/-- OOS:{Shelf4_1oos_data}\n"
data8=f"Shelf4_2/Wrong object :{Shelf4_2wrong_object_data}/-- SOOS:{Shelf4_2soos_data}/-- OOS:{Shelf4_2oos_data}\n"

message=message+data+data2+data3+data4+data5+data6+data7+data8
now=datetime.now()
day=now.day
month=now.month
year=now.year
hour=now.hour
minute=now.minute
second=now.second
message=message+f"date: {day}/{month}/{year} time: {hour}:{minute}:{second}\n"
gui.publish(gui.topic,message)
time.sleep(2)
gui.stop_mqtt()
print(message)