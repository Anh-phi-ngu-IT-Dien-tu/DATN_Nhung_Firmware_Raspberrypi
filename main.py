from Vision_Agorithm import *
import cv2
import threading
from Comparision_Agorithm import *
from robot_mqtt import Robot_MQTT_Position 



# below_cam=Vision_ESP32("http://192.168.137.124/capture","stockv14.pt","oosv8_20.3.pt",0.6,0.45)

# #test comparision
# Shelf1=Shelf({"247", "Chinsu", "ChocoPie", "D.Thanh", "Heineken", "Oreo"},1)

# Shelf1.shelf_object_comparision(1,'Pepsi-xanh',0,0,0)
# Shelf1.shelf_object_comparision(2,'ChocoPie',10,0,0)
# Shelf1.shelf_object_comparision(1,'ChocoPie',10,100,1)
# Shelf1.shelf_object_comparision(1,'Pepsi-xanh',10,150,1)
# Shelf1.shelf_object_comparision(1,'Pespi-den',30,-50,1)


# # Open and read the JSON file
# with open('Wrong_object_in_shelf_1.json', 'r') as file:
#     data = json.load(file)

# # Print the data
# print(data)


Shelf1_1=Shelf({'247', 'Chinsu', 'ChocoPie', 'D.Thanh', 'Heineken', 'Oreo'},1)
Shelf1_2=Shelf({'Pepsi-den', 'Pepsi-xanh', 'Redbull', 'Revive-chanh', 'Revive-trang', 'Simply', 'Tea Plus'},1)

Shelf1_pos=Shelf_Position(1000,1300,-1700,-500,-1.7,-1.3)
Shelf2_pos=Shelf_Position(-800,-500,-600,-100,1.4,1.8)
allow_model=0

above_cam=Vision(0,"stockv14.pt","oosv8_20.3.pt",0.6,0.45)
below_cam=Vision(2,"stockv14.pt","oosv8_20.3.pt",0.6,0.45,"Detection2","Out_of_stock_2")

Robot_Pos=Robot_MQTT_Position()
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
    while True:
        below_cam.Capture_frame()
        Shelf_Pos_Compare()
        if allow_model==1 or allow_model ==2:
            below_cam.Vision_Model()
            for label in below_cam.labels1:
                Shelf1_1.shelf_object_comparision(allow_model,label,Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
            

        print_out=f"{Robot_Pos.message} Shelf {allow_model}"
        below_cam.show_result(print_out)
        if cv2.waitKey(1)==ord('q'):
            break
   

def Cam2():
    global allow_model
    while True:
        above_cam.Capture_frame()
        if allow_model==1 or allow_model ==2:
            above_cam.Vision_Model()
            for label in above_cam.labels1:
                Shelf1_2.shelf_object_comparision(allow_model,label,Robot_Pos.x,Robot_Pos.y,Robot_Pos.theta)
        
        above_cam.show_result()
        if cv2.waitKey(1)==ord('q'):
            break
    

t1=threading.Thread(target=Cam1,daemon=True)
t2=threading.Thread(target=Cam2,daemon=True)


t1.start()
t2.start()


t1.join()
t2.join()


cv2.destroyAllWindows()
Robot_Pos.stop_mqtt()

