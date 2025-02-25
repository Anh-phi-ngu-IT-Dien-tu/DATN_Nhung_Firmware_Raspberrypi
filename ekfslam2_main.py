from ekfslam2 import EkfSlam
from my_lidar import MyLidar
from my_mcu import MyMCU
import numpy as np
import threading
import serial
import time
import json

def bluetooth_handler():
    bluetooth = serial.Serial("/dev/rfcomm0", 115200)
    while True:
        data = bluetooth.read().decode()
        if data == "f":
            mcu.write(50, 0)
        elif data == "l":
            mcu.write(0, np.pi/18)
        elif data == "r":
            mcu.write(0, -np.pi/18)
        elif data== "b":
            mcu.write(-50, 0)
        else:
            mcu.write(0, 0)

bluetooth_thread = threading.Thread(target=bluetooth_handler, daemon=True)
bluetooth_thread.start()

lidar = MyLidar("/dev/ttyUSB1")
lidar.start()

mcu = MyMCU("/dev/ttyUSB0", 115200)
mcu.start()

# Noise parameters
Q = [0.25, 0.25]
R = [0.15, np.deg2rad(2)]

robot = EkfSlam(min_range=150, max_range=2000, point_dist_threshold=10, min_cluster_size=5, max_cluster_size=30,
                avg_angles_lower_bound=np.deg2rad(120), avg_angles_upper_bound=np.deg2rad(160), std_angles_threshold=np.deg2rad(8),
                min_radius=30, max_radius=40, max_landmarks=20, Q=Q, R=R, maha_threshold=10.6, waypoint_min_distance=50)

n = 0
test1 = []
test2 = []

try:
    while True:
        time.sleep(0.05)
        dr, dl, b = mcu.read()
        robot.predict(dr, dl, b)
        scan = lidar.read()
        if len(scan) > 0:
            test1.append([n, robot.landmarks])
            test2.append([n, robot.mean[0, 0], robot.mean[1, 0], robot.mean[2, 0]])
            n += 1
            robot.extract_landmarks(scan)
            robot.correct()
        robot.add_waypoint()
        
except KeyboardInterrupt:
    lidar.stop()
    mcu.stop()
    robot.save_data()
    print(robot.mean)
    print(robot.known_lm)
    with open("test1.json", "w") as f:
        json.dump(test1, f)
    with open("test2.json", "w") as f:
        json.dump(test2, f)