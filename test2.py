from robot_mqtt import Robot_MQTT_Position 
import os
import shutil
import time
import json
import ast
from datetime import datetime
from Comparision_Agorithm import *
import threading


path="./shelves_information_report"

if not os.path.exists(path):
    os.mkdir(path)
elif os.path.exists(path):
    shutil.rmtree(path) 
    os.mkdir(path)

Shelf1_1=Shelf(["coca"],1,1,"shelf1_1",path)
Shelf1_2=Shelf([""],1,2,"shelf1_2",path)

Shelf2_1=Shelf([],2,1,"shelf2_1",path)
Shelf2_2=Shelf([],2,2,"shelf2_2",path)

Shelf3_1=Shelf([],3,1,"shelf3_1",path)
Shelf3_2=Shelf([],3,2,"shelf3_2",path)

Shelf4_1=Shelf([],4,1,"shelf4_1",path)
Shelf4_2=Shelf([],4,2,"shelf4_2",path)

Shelf1_pos=Shelf_Position(shelf_id=1,shelf_path=path)
Shelf2_pos=Shelf_Position(shelf_id=2,shelf_path=path)
Shelf3_pos=Shelf_Position(shelf_id=3,shelf_path=path)
Shelf4_pos=Shelf_Position(shelf_id=4,shelf_path=path)

allow_model=0
allow_model2=0
allow_model3 = 0
allow_model4 = 0
allow_cam1=0
allow_cam2=0
allow_cam3=0
allow_cam4=0
break_thread=False

gui=Robot_MQTT_Position(host="broker.emqx.io",topic="GUI",use_coordinate=False)
gui.start_mqtt()

time_start=time.time()
while gui.message==None:
    time_end=time.time()
    time.sleep(1)

a=gui.get_message().split('/')
robot_topic=None
for b in a:
    try:
        c = ast.literal_eval(b)
        Shelf1_1.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf1_2.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf1_pos.Load_shelf_position(c['Shelf'],c['From'],c['To'])
        Shelf2_1.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf2_2.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf2_pos.Load_shelf_position(c['Shelf'],c['From'],c['To'])
        Shelf3_1.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf3_2.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf3_pos.Load_shelf_position(c['Shelf'],c['From'],c['To'])
        Shelf4_1.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf4_2.Load_shelf_information(c['Shelf'],c['Sub shelf'],c['Product'])
        Shelf4_pos.Load_shelf_position(c['Shelf'],c['From'],c['To'])
    except:
        pass
gui_receive_topic=a[-1]
gui.publish(gui.topic,f"Yolo ready\n{gui_receive_topic}")
Shelf1_1.wrong_object_data=[
    {
        "object":"vinhhao"
    },
    {
        "object":"Chinsu"
    }
]

Shelf3_1.wrong_object_data=[
    {
        "object":"D.Thanh"
    },
    {
        "object":"Heineken"
    }
]

Shelf3_1.soos_data[""]=1

gui_receive=Robot_MQTT_Position(host="broker.emqx.io",topic=gui_receive_topic,use_coordinate=False)
gui_receive.start_mqtt()
def Shelf_Reset_Data(index=1):
    for i in range(1,3):
        Shelf1_1.ResetData(index,i)
        Shelf1_2.ResetData(index,i)
        Shelf2_1.ResetData(index,i)
        Shelf2_2.ResetData(index,i)
        Shelf3_1.ResetData(index,i)
        Shelf3_2.ResetData(index,i)
        Shelf4_1.ResetData(index,i)
        Shelf4_2.ResetData(index,i)


def Sending():
    global break_thread
    message=''
    while True:
        try:
            message=''         
            data= f"Shelf1_1/Wrong object :{Shelf1_1.wrong_object_data}/-- SOOS:{Shelf1_1.soos_data}/-- OOS:{Shelf1_1.oos_data}\n"
            data2=f"Shelf1_2/Wrong object :{Shelf1_2.wrong_object_data}/-- SOOS:{Shelf1_2.soos_data}/-- OOS:{Shelf1_2.oos_data}\n"
            data3=f"Shelf2_1/Wrong object :{Shelf2_1.wrong_object_data}/-- SOOS:{Shelf2_1.soos_data}/-- OOS:{Shelf2_1.oos_data}\n"
            data4=f"Shelf2_2/Wrong object :{Shelf2_2.wrong_object_data}/-- SOOS:{Shelf2_2.soos_data}/-- OOS:{Shelf2_2.oos_data}\n"
            data5=f"Shelf3_1/Wrong object :{Shelf3_1.wrong_object_data}/-- SOOS:{Shelf3_1.soos_data}/-- OOS:{Shelf3_1.oos_data}\n"
            data6=f"Shelf3_2/Wrong object :{Shelf3_2.wrong_object_data}/-- SOOS:{Shelf3_2.soos_data}/-- OOS:{Shelf3_2.oos_data}\n"
            data7=f"Shelf4_1/Wrong object :{Shelf4_1.wrong_object_data}/-- SOOS:{Shelf4_1.soos_data}/-- OOS:{Shelf4_1.oos_data}\n"
            data8=f"Shelf4_2/Wrong object :{Shelf4_2.wrong_object_data}/-- SOOS:{Shelf4_2.soos_data}/-- OOS:{Shelf4_2.oos_data}\n"
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
            time.sleep(1.2)
        except KeyboardInterrupt:
            break_thread=True
            break

def Receiving():
    global break_thread
    received_message=''
    while break_thread==False:
        if gui_receive.message!=None:
            received_message=gui_receive.get_message()
            if received_message.startswith("Shelf"):
                temp=received_message.replace("Shelf","")
                index=int(temp)
                Shelf_Reset_Data(index)
                           
            

t1=threading.Thread(target=Sending,daemon=True)
t2=threading.Thread(target=Receiving,daemon=True)
t1.start()
t2.start()
t1.join()
t2.join()


gui.stop_mqtt()
gui_receive.start_mqtt()






