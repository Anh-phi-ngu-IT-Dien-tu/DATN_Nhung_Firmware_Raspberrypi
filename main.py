from Vision_Agorithm import *
import cv2
import threading



below_cam=Vision_ESP32("http://192.168.137.124/capture","stockv14.pt","oosv8_20.3.pt",0.6,0.45)
above_cam=Vision(0,"stockv14.pt","oosv8_20.3.pt",0.6,0.45)

def Cam1():
    while True:
        below_cam.Capture_frame()
        below_cam.ESP32_Vision_Model()
        below_cam.show_result()
        if cv2.waitKey(1)==ord('q'):
            break

def Cam2():
    while True:
        above_cam.Capture_frame()
        above_cam.Vision_Model()
        above_cam.show_result()
        if cv2.waitKey(1)==ord('q'):
            break

t1=threading.Thread(target=Cam1,daemon=True)
t2=threading.Thread(target=Cam2,daemon=True)

t1.start()
t2.start()

t1.join()
t2.join()


