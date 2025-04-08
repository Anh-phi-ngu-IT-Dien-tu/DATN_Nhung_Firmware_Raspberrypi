from Vision_Agorithm import *
import cv2
import threading
from Comparision_Agorithm import *
from robot_mqtt import Robot_MQTT_Position 



Shelf1_1=Shelf(['custas', 'ChocoPie'],1,"shelf1_1")
Shelf1_2=Shelf(['coca', 'Pepsi-xanh', 'Vinamilk'],1,"shelf1_2")

Shelf1_pos=Shelf_Position(1000,1300,-1700,-500,-1.7,-1.3)
Shelf2_pos=Shelf_Position(-800,-500,-1000,-150,1.4,1.8)
allow_model=2
allow_model2=2
allow_cam1=0
allow_cam2=0
break_thread=False

above_cam=Vision_ESP32("http://192.168.137.245/capture","stockv18.pt","oosv11.pt",0.75,0.6,"Above_detection","Above_Out_of_stock")
below_cam=Vision_ESP32("http://192.168.137.148/capture","stockv18.pt","oosv11.pt",0.75,0.6,"Below_detection","Below_Out_of_stock")

Robot_Pos=Robot_MQTT_Position(host="broker.emqx.io")
Robot_Pos.start_mqtt()



def Shelf_Pos_Compare():
    global allow_model
    Shelf1_pos.compare_robot_shelf_position(Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
    Shelf2_pos.compare_robot_shelf_position(Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
    if Shelf1_pos.comparision_result==True and Shelf2_pos.comparision_result ==False:
        allow_model=1
    elif Shelf1_pos.comparision_result==False and Shelf2_pos.comparision_result ==True:
        allow_model=2
    else:
        allow_model=0

def Shelf_Pos_Compare2():
    global allow_model2
    Shelf1_pos.compare_robot_shelf_position(Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
    Shelf2_pos.compare_robot_shelf_position(Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
    if Shelf1_pos.comparision_result==True and Shelf2_pos.comparision_result ==False:
        allow_model2=1
    elif Shelf1_pos.comparision_result==False and Shelf2_pos.comparision_result ==True:
        allow_model2=2
    else:
        allow_model2=0

def Cam1():
    global allow_model
    global allow_cam1
    global break_thread
    while True:
        below_cam.Capture_frame()
        if allow_cam1>10:
            # Shelf_Pos_Compare()
            if allow_model==1 or allow_model ==2:
                below_cam.ESP32_Vision_Model()
                Shelf1_1.shelf_object_comparision(allow_model,below_cam.object_label_dict)
                Shelf1_1.semi_out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict,0.7)
                Shelf1_1.out_of_stock_checking(allow_model,below_cam.object_label_dict,below_cam.stock_stage_label_dict)

            print_out=f"{Robot_Pos.message} Shelf {allow_model}"
            below_cam.show_result(print_out)
            if cv2.waitKey(1)==ord('q') or break_thread==True:
                Shelf1_1.write_data_to_json()
                break_thread=True
                break
            continue
           
        allow_cam1+=1
            
   

def Cam2():
    global allow_model2
    global allow_cam2
    global break_thread
    while True:
        above_cam.Capture_frame()
        if allow_cam2>10:
            # Shelf_Pos_Compare2()
            if allow_model2==1 or allow_model2 ==2:
                above_cam.ESP32_Vision_Model()
                Shelf1_2.shelf_object_comparision(allow_model2,above_cam.object_label_dict)
                Shelf1_2.semi_out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict,0.7) 
                Shelf1_2.out_of_stock_checking(allow_model2,above_cam.object_label_dict,above_cam.stock_stage_label_dict)               
           
            print_out=f"{Robot_Pos.message} Shelf {allow_model2}"
            above_cam.show_result(print_out)
            if cv2.waitKey(1)==ord('q') or break_thread==True:
                Shelf1_2.write_data_to_json()
                break_thread=True
                break
            continue
        allow_cam2+=1    
                

t1=threading.Thread(target=Cam1,daemon=True)
t2=threading.Thread(target=Cam2,daemon=True)


t1.start()
t2.start()


t1.join()
t2.join()



cv2.destroyAllWindows()
Shelf1_1.write_data_to_json()
Shelf1_2.write_data_to_json()
Robot_Pos.stop_mqtt()

