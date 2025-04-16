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

path="./shelves_information_report"

if not os.path.exists(path):
    os.mkdir(path)
elif os.path.exists(path):
    shutil.rmtree(path) 
    os.mkdir(path)

Shelf1_1=Shelf(["coca"],1,1,"shelf1_1",path)
Shelf1_2=Shelf([],1,2,"shelf1_2",path)

Shelf2_1=Shelf([],2,1,"shelf2_1",path)
Shelf2_2=Shelf([],2,2,"shelf2_2",path)

Shelf3_1=Shelf([],3,1,"shelf3_1",path)
Shelf3_2=Shelf([],3,2,"shelf3_2",path)

Shelf4_1=Shelf([],4,1,"shelf4_1",path)
Shelf4_2=Shelf([],4,2,"shelf4_2",path)

Shelf1_pos=Shelf_Position(shelf_id=1)
Shelf2_pos=Shelf_Position(shelf_id=2)
Shelf3_pos=Shelf_Position(shelf_id=3)
Shelf4_pos=Shelf_Position(shelf_id=4)

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
    print(f"Currently time_start={time_end-time_start} and we have not received any thing")
    time.sleep(1)

print("We have received information")
a=gui.get_message().split('/')
print(a)
robot_topic=None
for b in a:
    try:
        c = ast.literal_eval(b)
        print(c['Product'])
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
print(f"{Shelf1_pos.x_below} {Shelf1_pos.y_below} {Shelf1_pos.theta_below} {Shelf1_pos.x_above} {Shelf1_pos.y_above} {Shelf1_pos.theta_above}")
print(f"{Shelf2_pos.x_below} {Shelf2_pos.y_below} {Shelf2_pos.theta_below} {Shelf2_pos.x_above} {Shelf2_pos.y_above} {Shelf2_pos.theta_above}")
gui.publish(gui.topic,a[-1])
robot_topic=a[-1]

Robot_Pos=Robot_MQTT_Position(host="broker.emqx.io",topic=robot_topic)
Robot_Pos.start_mqtt()

above_cam=Vision_ESP32("http://192.168.137.122/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Above_detection","Above_Out_of_stock")
below_cam=Vision_ESP32("http://192.168.137.98/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Below_detection","Below_Out_of_stock")
# above_cam2=Vision_ESP32("http://192.168.137.245/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Above_detection_2","Above_Out_of_stock_2")
# below_cam2=Vision_ESP32("http://192.168.137.148/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Below_detection_2","Below_Out_of_stock_2")



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


def Cam1():
    global allow_model
    global allow_cam1
    global break_thread
    while True:
        try:
            below_cam.Capture_frame()
            if allow_cam1>10:
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
                below_cam.show_result(print_out)
                if cv2.waitKey(1)==ord('q') or break_thread==True:
                    break_thread=True
                    break
                continue
            
            allow_cam1+=1
        except:
            print("Error cam 1")

def Cam2():
    global allow_model2
    global allow_cam2
    global break_thread
    while True:
        try:
            above_cam.Capture_frame()
            if allow_cam2>10:
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
                if cv2.waitKey(1)==ord('q') or break_thread==True:
                    break_thread=True
                    break
                continue
            allow_cam2+=1
        except:
            print("Error cam 2")


def Cam3():
    global allow_model3
    global allow_cam3
    global break_thread
    while True:
        above_cam2.Capture_frame()
        if allow_cam3 > 10:
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
            above_cam2.show_result(print_out)
            if cv2.waitKey(1) == ord('q') or break_thread==True:
                break_thread = True
                break
            continue
        allow_cam3 += 1


def Cam4():
    global allow_model4
    global allow_cam4
    global break_thread
    while True:
        below_cam2.Capture_frame()
        if allow_cam4 > 10:
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
            below_cam2.show_result(print_out)
            if cv2.waitKey(1) == ord('q') or break_thread:
                break_thread = True
                break
            continue
        allow_cam4 += 1


t1=threading.Thread(target=Cam1,daemon=True)
t2=threading.Thread(target=Cam2,daemon=True)


t1.start()
t2.start()


t1.join()
t2.join()



cv2.destroyAllWindows()
Shelf1_1.write_data_to_json()
Shelf2_1.write_data_to_json()
Shelf1_2.write_data_to_json()
Shelf2_2.write_data_to_json()
Shelf3_1.write_data_to_json()
Shelf3_2.write_data_to_json()
Shelf4_1.write_data_to_json()
Shelf4_2.write_data_to_json()
Robot_Pos.stop_mqtt()

message=''

for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            full_path = os.path.join(root, file)
            with open(full_path,"r") as readfile:
                data = json.load(readfile)
                message=message+f'{data}\n'

gui.publish(gui.topic,message)
print(message)
gui.stop_mqtt()
                        
                        