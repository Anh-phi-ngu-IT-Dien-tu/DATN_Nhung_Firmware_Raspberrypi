from Vision_Agorithm import *
import cv2
import threading
from Comparision_Agorithm import *
from robot_mqtt import Robot_MQTT_Position 


Shelf1_1=Shelf({'247', 'Chinsu', 'ChocoPie', 'D.Thanh', 'Heineken', 'Oreo'},1,"shelf1_1")
Shelf1_2=Shelf({'Pepsi-den', 'Pepsi-xanh', 'Redbull', 'Revive-chanh', 'Revive-trang', 'Simply', 'Tea Plus'},1,"shelf1_2")

Shelf1_pos=Shelf_Position(1000,1300,-1700,-500,-1.7,-1.3)
Shelf2_pos=Shelf_Position(-800,-500,-600,-100,1.4,1.8)
allow_model=0
allow_cam1=0
allow_cam2=0
break_threading=0

above_cam=Vision(0,"stockv14.pt","oosv8_20.3.pt",0.6,0.45,"Above_detection","Above_Out_of_stock")
below_cam=Vision(2,"stockv14.pt","oosv8_20.3.pt",0.6,0.45,"Below_detection","Below_Out_of_stock")

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


def Cam1():
    global allow_model
    global allow_cam1
    global break_threading
    while True:
        below_cam.Capture_frame()
        if allow_cam1>10:
            Shelf_Pos_Compare()
            if allow_model==1 or allow_model ==2:
                below_cam.Vision_Model()
                for label in below_cam.labels1:
                    Shelf1_1.shelf_object_comparision(allow_model,label,Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
                    
                

            print_out=f"{Robot_Pos.message} Shelf {allow_model}"
            below_cam.show_result(print_out)
            if cv2.waitKey(1)==ord('q'):
                Shelf1_1.write_data_to_json()
                break_threading=1
                break
            continue
           
        allow_cam1+=1
            
   

def Cam2():
    global allow_model
    global allow_cam2
    global break_threading
    while True:
        above_cam.Capture_frame()
        if allow_cam2>10:
            if allow_model==1 or allow_model ==2:
                above_cam.Vision_Model()
                for label in above_cam.labels1:
                    Shelf1_2.shelf_object_comparision(allow_model,label,Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
            
            above_cam.show_result()
            if cv2.waitKey(1)==ord('q') or break_threading==1:
                Shelf1_2.write_data_to_json()
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
Robot_Pos.stop_mqtt()

