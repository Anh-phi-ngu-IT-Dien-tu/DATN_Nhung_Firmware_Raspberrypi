#from Vision_Agorithm import *
import cv2
import threading
from Comparision_Agorithm import *
from Vision_Agorithm import Vision_ESP32
from robot_mqtt import Robot_MQTT_Position 
import os
import shutil
import time
import json
import ast
from datetime import datetime

path="./shelves_information_report"

if not os.path.exists(path):
    os.mkdir(path)
elif os.path.exists(path):
    shutil.rmtree(path) 
    os.mkdir(path)



Shelf1_1=Shelf([],1,1,"shelf1_1",path)
Shelf1_2=Shelf([],1,2,"shelf1_2",path)

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

gui_receive=Robot_MQTT_Position(host="broker.emqx.io",topic=gui_receive_topic,use_coordinate=False)
gui_receive.start_mqtt()
Robot_Pos=Robot_MQTT_Position(host="broker.emqx.io",topic="Robot")
Robot_Pos.start_mqtt()

above_cam=Vision_ESP32("http://192.168.137.235/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf1,2_2 detection","Shelf1,2_2 out_of_stock")
below_cam=Vision_ESP32("http://192.168.137.138/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf1,2_1 detection","Shelf1,2_1 out_of_stock")
above_cam2=Vision_ESP32("http://192.168.137.245/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf3,4_2 detection","Shelf3,4_2 out_of_stock")
below_cam2=Vision_ESP32("http://192.168.137.26/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf3,4_1 detection","Shelf3,4_1 out_of_stock")



def Shelf_Pos_Compare():
    global allow_model
    Shelf1_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    Shelf2_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    # Add logic for additional shelves
   
    if Shelf1_pos.comparision_result==True and Shelf2_pos.comparision_result==False:
        allow_model = 1
    elif Shelf2_pos.comparision_result==True and Shelf1_pos.comparision_result==False:
        allow_model = 2
    else:
        allow_model = 0

def Shelf_Pos_Compare2():
    global allow_model2
    Shelf1_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    Shelf2_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    # Add logic for additional shelves
  

    if Shelf1_pos.comparision_result==True and Shelf2_pos.comparision_result==False:
        allow_model2 = 1
    elif Shelf2_pos.comparision_result==True and Shelf1_pos.comparision_result==False:
        allow_model2 = 2
    else:
        allow_model2 = 0

def Shelf_Pos_Compare3():
    global allow_model3
    Shelf3_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    Shelf4_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)

    if Shelf3_pos.comparision_result and not Shelf4_pos.comparision_result:
        allow_model3 = 3
    elif Shelf4_pos.comparision_result and not Shelf3_pos.comparision_result:
        allow_model3=4
    else:
        allow_model3 = 0

def Shelf_Pos_Compare4():
    global allow_model4
    Shelf3_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)
    Shelf4_pos.compare_robot_shelf_position(Robot_Pos.x, Robot_Pos.y, Robot_Pos.theta)

    if Shelf3_pos.comparision_result and not Shelf4_pos.comparision_result:
        allow_model4 = 3
    elif Shelf4_pos.comparision_result and not Shelf3_pos.comparision_result:
        allow_model4 = 4
    else:
        allow_model4 = 0

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

def Cam1():
    global allow_model
    global break_thread
    while True:
        try:
            below_cam.Capture_frame()        
            Shelf_Pos_Compare()
            if allow_model==1 or allow_model ==2:
                below_cam.ESP32_Vision_Model()
                Shelf1_1.shelf_object_comparision(allow_model,below_cam.object_label_dict)
                Shelf1_1.semi_out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict,0.7)
                Shelf1_1.out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict)

                Shelf2_1.shelf_object_comparision(allow_model,below_cam.object_label_dict)
                Shelf2_1.semi_out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict,0.7)
                Shelf2_1.out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict)
                
                Shelf1_1.seen_product_checking(allow_model,below_cam.object_label_dict)
                Shelf2_1.seen_product_checking(allow_model,below_cam.object_label_dict)

            elif allow_model==0:
                Shelf1_1.seen_product_checking(allow_model,below_cam.object_label_dict)
                Shelf2_1.seen_product_checking(allow_model,below_cam.object_label_dict)


            print_out=f"{Robot_Pos.message} Shelf {allow_model}"
            below_cam.show_result(print_out,False,False)
            if cv2.waitKey(25)==ord('q') or break_thread==True:
                break_thread=True
                Shelf1_1.write_data_to_json()
                Shelf2_1.write_data_to_json()
                break
            continue
        except KeyboardInterrupt:
            Shelf1_1.write_data_to_json()
            Shelf2_1.write_data_to_json()
            pass

def Cam2():
    global allow_model2
    global break_thread
    while True:
        try:
            above_cam.Capture_frame()
            Shelf_Pos_Compare2()
            if allow_model2==1 or allow_model2 ==2:
                above_cam.ESP32_Vision_Model()
                Shelf1_2.shelf_object_comparision(allow_model2,above_cam.object_label_dict)
                Shelf1_2.semi_out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict,0.7) 
                Shelf1_2.out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict)        

                Shelf2_2.shelf_object_comparision(allow_model2,above_cam.object_label_dict)
                Shelf2_2.semi_out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict,0.7) 
                Shelf2_2.out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict)                      

                Shelf1_2.seen_product_checking(allow_model2,above_cam.object_label_dict)
                Shelf2_2.seen_product_checking(allow_model2,above_cam.object_label_dict)

            elif allow_model2==0:
                Shelf1_2.seen_product_checking(allow_model2,above_cam.object_label_dict)
                Shelf2_2.seen_product_checking(allow_model2,above_cam.object_label_dict)
            

            print_out=f"{Robot_Pos.message} Shelf {allow_model2}"
            above_cam.show_result(print_out)
            if cv2.waitKey(25)==ord('q') or break_thread==True:
                break_thread=True
                Shelf1_2.write_data_to_json()
                Shelf2_2.write_data_to_json()
                break
            continue
        except KeyboardInterrupt:
            Shelf1_2.write_data_to_json()
            Shelf2_2.write_data_to_json()
            pass


def Cam3():
    global allow_model3
    global break_thread
    while True:
        try:
            above_cam2.Capture_frame()
            Shelf_Pos_Compare3()
            if allow_model3 == 3 or allow_model3 == 4:
                above_cam2.ESP32_Vision_Model()
                Shelf3_2.shelf_object_comparision(allow_model3, above_cam2.object_label_dict)
                Shelf3_2.semi_out_of_stock_checking(allow_model3, above_cam2.object_label_dict, above_cam2.stock_stage_label_dict, 0.7)
                Shelf3_2.out_of_stock_checking(allow_model3, above_cam2.object_label_dict, above_cam2.stock_stage_label_dict)

                Shelf4_2.shelf_object_comparision(allow_model3, above_cam2.object_label_dict)
                Shelf4_2.semi_out_of_stock_checking(allow_model3, above_cam2.object_label_dict, above_cam2.stock_stage_label_dict, 0.7)
                Shelf4_2.out_of_stock_checking(allow_model3, above_cam2.object_label_dict, above_cam2.stock_stage_label_dict)

                Shelf3_2.seen_product_checking(allow_model3, above_cam2.object_label_dict)
                Shelf4_2.seen_product_checking(allow_model3, above_cam2.object_label_dict)

            elif allow_model3 == 0:
                Shelf3_2.seen_product_checking(allow_model3, above_cam2.object_label_dict)
                Shelf4_2.seen_product_checking(allow_model3, above_cam2.object_label_dict)

            print_out = f"{Robot_Pos.message} Shelf {allow_model3}"
            above_cam2.show_result(print_out,False,False)
            if cv2.waitKey(25) == ord('q') or break_thread==True:
                break_thread = True
                Shelf3_2.write_data_to_json()
                Shelf4_2.write_data_to_json()
                break
            continue
        except KeyboardInterrupt:
            Shelf3_2.write_data_to_json()
            Shelf4_2.write_data_to_json()
            pass


def Cam4():
    global allow_model4
    global break_thread
    while True:
        try:
            below_cam2.Capture_frame()
            Shelf_Pos_Compare4()
            if allow_model4 == 3 or allow_model4 == 4:
                below_cam2.ESP32_Vision_Model()
                Shelf3_1.shelf_object_comparision(allow_model4, below_cam2.object_label_dict)
                Shelf3_1.semi_out_of_stock_checking(allow_model4, below_cam2.object_label_dict, below_cam2.stock_stage_label_dict, 0.7)
                Shelf3_1.out_of_stock_checking(allow_model4, below_cam2.object_label_dict, below_cam2.stock_stage_label_dict)

                Shelf4_1.shelf_object_comparision(allow_model4, below_cam2.object_label_dict)
                Shelf4_1.semi_out_of_stock_checking(allow_model4, below_cam2.object_label_dict, below_cam2.stock_stage_label_dict, 0.7)
                Shelf4_1.out_of_stock_checking(allow_model4, below_cam2.object_label_dict, below_cam2.stock_stage_label_dict)

                Shelf3_1.seen_product_checking(allow_model4, below_cam2.object_label_dict)
                Shelf4_1.seen_product_checking(allow_model4, below_cam2.object_label_dict)

            elif allow_model4 == 0:
                Shelf3_1.seen_product_checking(allow_model4, below_cam2.object_label_dict)
                Shelf4_1.seen_product_checking(allow_model4, below_cam2.object_label_dict)

            print_out = f"{Robot_Pos.message} Shelf {allow_model4}"
            below_cam2.show_result(print_out,False,False)
            if cv2.waitKey(25) == ord('q') or break_thread:
                break_thread = True
                Shelf3_1.write_data_to_json()
                Shelf4_1.write_data_to_json()
                break
            continue
        except KeyboardInterrupt:
            Shelf3_1.write_data_to_json()
            Shelf4_1.write_data_to_json()
            pass

def Sending():
    global break_thread
    message=''
    while break_thread==False:
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
        time.sleep(2)

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
        time.sleep(1)
            
            

t1=threading.Thread(target=Cam1,daemon=True)
t2=threading.Thread(target=Cam2,daemon=True)
t3=threading.Thread(target=Cam3,daemon=True)
t4=threading.Thread(target=Cam4,daemon=True)
t5=threading.Thread(target=Sending,daemon=True)
t6=threading.Thread(target=Receiving,daemon=True)
 

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()



cv2.destroyAllWindows()
Robot_Pos.stop_mqtt()

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
gui_receive.stop_mqtt()
                        
                        