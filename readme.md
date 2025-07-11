#  Shelves store monitoring robot

## Introduction
This project focus on creating a mobile robot that can monitor shelves information like the shortage of goods, or misplaced goods 

## Contributors
- Vu Quoc Khanh : EKF SLAM, EKF Localization, Path-tracking algorithm
- Dao Anh Phi : Circuit design, STM32F103C8T6 firmware, GUI with QT5 on python
- Dang Van Vinh : Camera handling, image processing algorithm, Yolov8 model, Yolov8 training data
  
## Features
- Using 2-wheel mobile robot
- Speed control with STM32F103C8T6
- Lidar with Extended Kalman Filter SLAM algorithm for creating features map and define path for robot movement, Extended Kalman Filter localization for position tracking, path-tracking algorithm
- ESP32 Camera for gathering shelves information
- Using Yolov8 model combining with robot position to determine shelves states 
- A gui based on QT5 framework for observing the state of the shelves in real-time, toggling the states of the shelf 

## System Overview
### Block Diagram
![alt text](assets-images/image.png)
![alt text](assets-images/image-1.png)

### Components
- **Microcontroller**: STM32F103C8T6
- **Motor**: JGB37-520 12V 37RPM
- **Power Supply**: 3S 45C Lipo-battery
- **Power Regulator**: LM2596S
- **Embedded computer**: Raspberry Pi 4
- **Observation sensor**:RPLidar A1
- **Camera**: ESP32 Camera

## Hardware Design
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Motor_PCB_Design
![alt text](assets-images/image-2.png)

## Software Design
### Android app for controlling robot while defining map, robot path
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Android_app
### STM32F103C8T6 Firmware
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Motor
![alt text](assets-images/image-10.png)
![alt text](assets-images/image-3.png)
### EKF Algorithm (On Raspberry pi 4):
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Raspberrypi
![alt text](assets-images/image-4.png)
#### Feature extraction (On Raspberry pi 4):
![alt text](assets-images/image-5.png)
#### EKF SLAM for defining map, robot path
![alt text](assets-images/image-6.png)
#### EKF Localization for tracking robot positiom
![alt text](assets-images/image-7.png)
#### Path-tracking with P controller
![alt text](assets-images/image-8.png)
![alt text](assets-images/image-9.png)
### Image processing algorithm
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Vision_Part
#### Camera handling algorithm
![alt text](assets-images/image-11.png)
#### Yolov8 data 
![alt text](assets-images/image-12.png)
#### Yolov8 models, classes
- **Object detection model**: 21 class: 247, Chinsu, ChocoPie, D.Thanh, Heineken, Oreo, Pepsi-xanh, Redbull, Revive-chanh,Simply, TH true Milk, Tea Plus, Vinamilk, coca, coca-chai, custas, fanta-cam, khongdo, number1, sting, vinhhao
- **Almost out, out detection**: 2 class: oos (Out of stock) and semi-oos (Semi out of stock)
### GUI
https://github.com/Anh-phi-ngu-IT-Dien-tu/DATN_Nhung_Firmware_Raspberrypi/tree/Python_GUI 
![alt text](assets-images/image-13.png)

## Landmark
![alt text](assets-images/image-14.png)

## Results and Evaluation
https://youtu.be/jIvI4DPsrL0?si=AIefCEjHjDwL9q_E

### Usage
#### Prepare the power source
- Plug the LIPO batteries into the existing jack
- Connect 5V/3A power source(Portable charger)
- Check the connection between CH340G module to Raspberry pi 4, between RPLIDAR A1 to Raspberry pi 4
#### Draw map and robot path
- Download the Android app that in App to smart phone
- Setup Raspberry pi through headless connection
- Setup bluetooth connect by following this tutorial : https://youtu.be/sY06F_sPef4?si=ksDs4zLhg-ldZGuX
- Connect the android app and raspberry pi through bluetooth connection
- Run Raspberrypi/ekfslam2_main.py, wait for a few second, then control the robot through android app
- After creating feature-based map (which is saved_landmarks.json file), compare all features exist in map with real landmarks, remove all dupicated, wrong features.
#### Run localziation and path tracking algorithm
- (Optional) Modify the waypoints exist in waypoints.json
- Run localization2_main.py, the robot will follow the waypoint defined in waypoints.json, stop the robot when it meet the last waypoint
#### Run the vision algorithm
- (Pass this step if you have already done it)Config the wifi inside Vision\CameraWebServer\CameraWebServer.ino
```cpp
// ===========================
// 🔹 Nhập WiFi Credentials
// ===========================
const char *ssid = "LAPTOP-Phi";
const char *password = "Phi18112003Laptop";

```
- (Pass this step if you have already done it) Upload the Vision\CameraWebServer\CameraWebServer.ino to esp32 camera
- Get the IP address of the camera (reset the camera in order to load the ip address)
- Config the IP address in Vision\main_ver2.py
```python

above_cam=Vision_ESP32("http://192.168.137.235/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf1,2_2 detection","Shelf1,2_2 out_of_stock")
below_cam=Vision_ESP32("http://192.168.137.138/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf1,2_1 detection","Shelf1,2_1 out_of_stock")
above_cam2=Vision_ESP32("http://192.168.137.245/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf3,4_2 detection","Shelf3,4_2 out_of_stock")
below_cam2=Vision_ESP32("http://192.168.137.26/capture","stockv19.pt","oosv12.pt",0.75,0.6,"Shelf3,4_1 detection","Shelf3,4_1 out_of_stock")

```
- Run Vision\main_ver2.py on a laptop that use the same ip address of ESP32 camera
#### Setup GUI (proceed this before running localziation and path tracking algorithm and after running Vision\main_ver2.py)
- Run Python_GUI/datn_gui_handle.py 
- Define shelves object, coordinate so the vision algorithms can determine the shelves states
- (Optional but not recommended)Config the MQTT topic 
- Press Connect
- Press setting to send the shelves information and start running Yolov8 models and shelves states determination algorithm
- Watch the result appears on Watch shelves section
- (Optional) Press Fixed button if you think that the related shelf in Watch shelves section has been handled

### Advantages
- Reducing observation cost
- Yolov8 model can work with high confidence
- Robot can move around the store the way we want

### Limitations
- Time consumption for setup steps
- There are some small error for feature-based landmark 
- The path-defining algorithm is too dependent to the operation who controlling the robot with bluetooth app
- The overall image processing algorithm can not determine the complicated situations
- The GUI still not enough user-friendly

