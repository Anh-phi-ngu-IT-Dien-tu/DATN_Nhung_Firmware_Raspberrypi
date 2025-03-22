import cv2
import numpy as np
import urllib.request
from ultralytics import YOLO
import copy
import paho.mqtt.client as mqtt
import json


shelf1_1 = {"coca-cola","",""}
shelf1_2 = {"","",""}
shelf2_1 = {"","",""}
shelf2_2 ={"","",""}
shelfn_1=set({})
shelfn_2=set({})
wrong_detection_shelf1_1={}
wrong_detection_shelf1_2={}
wrong_detection_shelf2_1={}
wrong_detection_shelf2_2={}

# wrong_detection={"wrong_dêtction_shelf1_1"}

# shelf1_x_below =1100
# shelf1_x_above =1200
# shelf1_y_below =-600
# shelf1_y_above =-1600
# shelf1_theta_below=
# shelf1_theta_above=

# shelf2_x_below =-500
# shelf2_x_above =-700
# shelf2_y_below =-600
# shelf2_y_above =-170
# shelf1_theta_below=1.5
# shelf1_theta_above=1.7

shelf1_x_below =1000
shelf1_x_above =1300
shelf1_y_below =-1700
shelf1_y_above =-500
shelf1_theta_below=-1.7
shelf1_theta_above=-1.3

shelf2_x_below =-800
shelf2_x_above =-500
shelf2_y_below =-600
shelf2_y_above =-100
shelf2_theta_below=1.4
shelf2_theta_above=1.8


urlL = "http://192.168.137.242/capture"  # URL for the left camera
urlR = "http://192.168.137.148/capture"  # URL for the right camera (assuming it's different)
model = YOLO("stockv14.pt")  # Load the YOLO model
model_oos = YOLO("oosv8_20.3.pt")
message=""

allow_model=0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # topic
    client.subscribe("Robot")
    



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Do something else
    global message
    message=str(msg.payload.decode("utf-8"))
    
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect(host="test.mosquitto.org",port=1883)
client.loop_start()

while True:
    # Capture frame from the left camera
    img_respL = urllib.request.urlopen(urlL)
    imgnpL = np.array(bytearray(img_respL.read()), dtype=np.uint8)
    imgL = cv2.imdecode(imgnpL, -1)

    imgL_oos= copy.deepcopy(imgL)

    # Capture frame from the right camera
    img_respR = urllib.request.urlopen(urlR)
    imgnpR = np.array(bytearray(img_respR.read()), dtype=np.uint8)
    imgR = cv2.imdecode(imgnpR, -1)
    imgR_oos= copy.deepcopy(imgR)

    allow_model=0
    ##Xử lý vị trí robot có hợp lý để detect hay không
    if message !="":
        temp_message=message.split('/')
        x=float(temp_message[0])
        y=float(temp_message[1])
        theta=float(temp_message[2])
        

    ##Nếu đã hợp lý thì xét camera đang nhìn kệ hàng nào
        if shelf1_x_below<=x<=shelf1_x_above and shelf1_y_below<=y<=shelf1_y_above and shelf1_theta_below<=theta<=shelf1_theta_above:
            shelfn_1=shelf1_1
            shelfn_2=shelf1_2
            allow_model=1
        elif shelf2_x_below<=x<=shelf2_x_above and shelf2_y_below<=y<=shelf2_y_above and shelf2_theta_below<=theta<=shelf2_theta_above:
            shelfn_1=shelf2_1
            shelfn_2=shelf2_2
            allow_model=2
        else :
            shelfn_1=set({})
            shelfn_2=set({})
            allow_model=0
        print(x,y,theta,allow_model)
    print_message=f"{message} shelf {allow_model}"
    cv2.putText(imgL,print_message,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),1)
    allow_model=1
    # Perform object detection on left camera
    if allow_model==1 or allow_model ==2:
        resultsL = model(imgL, conf=0.6)
        
        for result in resultsL:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model.names[cls]}: {conf:.2f}"

                # Draw bounding boxes and labels on the left camera frame
                cv2.rectangle(imgL, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(imgL, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)                
                # if(model.names[cls] in shelfn_1):
                #     pass
                # else: 
                    
                #     pass
                        

                
        # out_pro_L.write(imgL)
        resultsL_oos = model_oos(imgL_oos, conf=0.45)
        for result in resultsL_oos:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model_oos.names[cls]}: {conf:.2f}"

                # Gán màu cho từng lớp
                if model_oos.names[cls] == 'oos':
                    color = (0, 255, 0)  # Màu xanh cho oos
                elif model_oos.names[cls] == 'semi-oos':
                    color = (0, 0, 255)  # Màu đỏ cho semi-oos
                else:
                    color = (255, 255, 255)  # Màu mặc định (trắng) cho các lớp khác

                # Vẽ bounding box và label với màu tương ứng
                cv2.rectangle(imgL_oos, (x1, y1), (x2, y2), color, 2)
                cv2.putText(imgL_oos, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1)



        # Perform object detection on right camera
        resultsR = model(imgR, conf=0.6)

        for result in resultsR:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model.names[cls]}: {conf:.2f}"

                # Draw bounding boxes and labels on the right camera frame
                cv2.rectangle(imgR, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(imgR, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

        # Stack both frames (left and right) side by side
    

        resultsR_oos = model_oos(imgR_oos, conf=0.45)
        for result in resultsR_oos:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{model_oos.names[cls]}: {conf:.2f}"

                # Gán màu cho từng lớp
                if model_oos.names[cls] == 'oos':
                    color = (0, 255, 0)  # Màu xanh cho oos
                elif model_oos.names[cls] == 'semi-oos':
                    color = (0, 0, 255)  # Màu đỏ cho semi-oos
                else:
                    color = (255, 255, 255)  # Màu mặc định (trắng) cho các lớp khác

                # Vẽ bounding box và label với màu tương ứng
                cv2.rectangle(imgR_oos, (x1, y1), (x2, y2), color, 2)
                cv2.putText(imgR_oos, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 1)

    
    # Write the combined frame to the output video


    imgL_frame= cv2.resize(imgL, (800,600))
    
    imgL_frame_oos= cv2.resize(imgL_oos, (800,600))
    imgR_frame= cv2.resize(imgR, (800,600))
    imgR_frame_oos= cv2.resize(imgR_oos, (800,600))
    # Display the combined frame
    cv2.imshow("YOLOv8 Detection Above",imgL_frame)
    cv2.imshow("YOLOv8 oos Above", imgL_frame_oos)
    cv2.imshow("YOLOv8 Detection below",imgR_frame)
    cv2.imshow("YOLOv8 oos below", imgR_frame_oos)
    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video writer and close windows
cv2.destroyAllWindows()
client.loop_stop()
