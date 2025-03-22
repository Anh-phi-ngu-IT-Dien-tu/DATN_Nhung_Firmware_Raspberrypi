import cv2
import numpy as np
import urllib.request
from ultralytics import YOLO
import threading
import random
import json
import copy
import time

class Vision:
    def __init__(self,camera_source=0,detetion_model="yolo11n.pt",out_of_stock_model="yolo11n.pt",detection_confidence=0.6,out_of_stock_confindence=0.45,detection_window_title="Detection",out_of_stock_window_title="Out_of_stock",json_file='Data.json'):
        self.camera_source=camera_source
        self.detection_model=YOLO(detetion_model)
        self.oos_model=YOLO(out_of_stock_model)
        self.capture=cv2.VideoCapture(camera_source)
        self.detection_conf=detection_confidence
        self.oos_conf=out_of_stock_confindence
        self.frame=None
        self.frame2=None
        self.outframe=None
        self.outframe2=None
        self.ret=None
        self.color = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(22)]
        self.detection_window=detection_window_title
        self.oos_window=out_of_stock_window_title
        self.json_file=json_file
        self.run=False
        # self.thread=threading.Thread(target=self.process_agorithm)
        self.t2=threading.Thread(target=self.Vision_Thread,daemon=True)
        pass
    
    def Capture_frame(self):
        self.ret,self.frame=self.capture.read()
        self.frame2=copy.deepcopy(self.frame)

    def Vision_Model(self):
        results=self.detection_model(self.frame,conf=self.detection_conf)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{self.detection_model.names[cls]}: {conf:.2f}"
                color=self.color[cls]
                # Draw bounding boxes and labels on the camera frame
                cv2.rectangle(self.frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(self.frame, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2)


        result_oos = self.oos_model(self.frame2,conf=self.oos_conf)
        for result in result_oos:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{self.oos_model.names[cls]}: {conf:.2f}"

                # Gán màu cho từng lớp
                if self.oos_model.names[cls] == 'oos':
                    color = (0, 255, 0)  # Màu xanh cho oos
                elif self.oos_model.names[cls] == 'semi-oos':
                    color = (0, 0, 255)  # Màu đỏ cho semi-oos
                else:
                    color = (255, 255, 255)  # Màu mặc định (trắng) cho các lớp khác

                # Vẽ bounding box và label với màu tương ứng
                cv2.rectangle(self.frame2, (x1, y1), (x2, y2), color, 2)
                cv2.putText(self.frame2, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1)

    
    def show_result(self):
        self.outframe= cv2.resize(self.frame, (800,600))
        self.outframe2= cv2.resize(self.frame2, (800,600))
        cv2.imshow(self.detection_window,self.outframe)
        cv2.imshow(self.oos_window, self.outframe2)
        pass
    
    def start_agorithm(self):
        self.run=True      
        self.t2.start()

    def stop_agorithm(self):
        self.t2.join()


    def Vision_Thread(self):
        while self.run ==True :
            self.Capture_frame()
            self.Vision_Model()
            self.show_result()
            if cv2.waitKey(1)==ord('q'):
                self.run=False
    




class Vision_ESP32:
    def __init__(self,esp_32_url="http://192.168.137.161/capture",detetion_model="yolo11n.pt",out_of_stock_model="yolo11n.pt",detection_threshold_confidence=0.6,out_of_stock_confidence=0.4,detection_window_title="ESP32_Detection",out_of_stock_window_title="ESP32_Out_of_stock",json_file='Data.json'):
        self.url=esp_32_url
        self.detection_model=YOLO(detetion_model)
        self.oos_model=YOLO(out_of_stock_model)
        self.detection_conf=detection_threshold_confidence
        self.oos_conf=out_of_stock_confidence
        self.img_esp=None
        self.imgnp=None
        self.img=None
        self.img2=None
        self.model_img=None
        self.model_img2=None
        self.out_img=None
        self.out_img2=None
        self.detection_window=detection_window_title
        self.oos_window=out_of_stock_window_title
        self.json_file=json_file
        self.run=False
        self.t2=threading.Thread(target=self.ESP32_Vision_Thread,daemon=True)
        self.i=0
        self.ct=False
        pass
    
    def Capture_frame(self):
        self.img_esp = urllib.request.urlopen(self.url)
        self.imgnp = np.array(bytearray(self.img_esp.read()), dtype=np.uint8)
        self.img = cv2.imdecode(self.imgnp, -1)
        self.img2=copy.deepcopy(self.img)

    def ESP32_Vision_Model(self):
        results=self.detection_model(self.img,conf=self.detection_conf)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{self.detection_model.names[cls]}: {conf:.2f}"
                # Draw bounding boxes and labels on the camera frame
                cv2.rectangle(self.img, (x1, y1), (x2, y2), (255,0,0), 2)
                cv2.putText(self.img, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)


        result_oos = self.oos_model(self.img2,conf=self.oos_conf)
        for result in result_oos:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = f"{self.oos_model.names[cls]}: {conf:.2f}"

                # Gán màu cho từng lớp
                if self.oos_model.names[cls] == 'oos':
                    color = (0, 255, 0)  # Màu xanh cho oos
                elif self.oos_model.names[cls] == 'semi-oos':
                    color = (0, 0, 255)  # Màu đỏ cho semi-oos
                else:
                    color = (255, 255, 255)  # Màu mặc định (trắng) cho các lớp khác

                # Vẽ bounding box và label với màu tương ứng
                cv2.rectangle(self.img2, (x1, y1), (x2, y2), color, 2)
                cv2.putText(self.img2, label, (x1, y1 - 50), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1)

        


    def show_result(self):
        self.out_img= cv2.resize(self.img, (800,600))
        self.out_img2= cv2.resize(self.img2, (800,600))
        cv2.imshow(self.detection_window,self.out_img)
        cv2.imshow(self.oos_window, self.out_img2)
        pass

    
    def start_agorithm(self):
        self.run=True
        self.t2.start()

    def stop_agorithm(self):
        self.t2.join()        


    def ESP32_Vision_Thread(self):
        while self.run==True:
            self.Capture_frame()
            self.ESP32_Vision_Model()
            self.show_result()
            if cv2.waitKey(1)==ord('q'):
                self.run=False
            


   