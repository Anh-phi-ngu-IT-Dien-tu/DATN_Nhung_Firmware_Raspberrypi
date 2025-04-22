from localization2 import Localization
from my_lidar import MyLidar
from my_mcu import MyMCU
import numpy as np
import threading
import serial
import time

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
        else:
            mcu.write(0, 0)

bluetooth_thread = threading.Thread(target=bluetooth_handler, daemon=True)
bluetooth_thread.start()

lidar = MyLidar("/dev/ttyUSB1")
lidar.start()

mcu = MyMCU("/dev/ttyUSB0", 115200)
mcu.start()

# Noise parameters
Q = [0.8, 0.8]
R = [0.01, np.deg2rad(1)]

robot = Localization(min_range=0, max_range=2000, point_dist_threshold=12, min_cluster_size=6, max_cluster_size=25,
                     avg_angles_lower_bound=np.deg2rad(120), avg_angles_upper_bound=np.deg2rad(160),
                     std_angles_threshold=np.deg2rad(6), min_radius=42, max_radius=47, Q=Q, R=R, maha_threshold=5.991,
                     linear_vel_max=10, turn_vel_max=5, waypoint_range=50, kp_dist=1, kp_heading=1,
                     waypoint_min_distance=150)

robot.load_landmarks()

try:
    while True:
        time.sleep(0.05)
        scan = lidar.read()
        dr, dl, b = mcu.read()
        robot.predict(dr, dl, b)
        if len(scan) > 0:
            robot.extract_landmarks(scan)
            robot.correct()
            print(robot.test)
            robot.add_waypoint()
        
except KeyboardInterrupt:
    lidar.stop()
    mcu.stop()
    robot.save_waypoints()
    print(robot.mean)