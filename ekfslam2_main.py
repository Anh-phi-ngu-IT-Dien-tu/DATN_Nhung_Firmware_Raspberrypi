from ekfslam2 import EkfSlam
from my_lidar import MyLidar
from my_mcu import MyMCU
import numpy as np
import threading
import serial
import time

def bluetooth_handler():
    bluetooth = serial.Serial("COM4", 115200)
    while True:
        data = bluetooth.read().decode()
        if data == "f":
            mcu.write(10, 0)
        elif data == "l":
            mcu.write(-5, 5)
        elif data == "r":
            mcu.write(5, -5)
        else:
            mcu.write(0, 0)

bluetooth_thread = threading.Thread(target=bluetooth_handler, daemon=True)
bluetooth_thread.start()

lidar = MyLidar("COM10")
lidar.start()

mcu = MyMCU("COM3", 115200)
mcu.start()

# Noise parameters
Q = [0.1, 0.1]
R = [0.1, np.deg2rad(1)]

robot = EkfSlam(min_range=150, max_range=4000, point_dist_threshold=10, min_cluster_size=10, max_cluster_size=40,
                avg_angles_lower_bound=np.deg2rad(120), avg_angles_upper_bound=np.deg2rad(160), std_angles_threshold=np.deg2rad(8),
                min_radius=30, max_radius=40, max_landmarks=2, Q=Q, R=R, maha_threshold=9, waypoint_min_distance=300)

try:
    while True:
        scan = lidar.read()
        if len(scan) > 0:
            robot.extract_landmarks(scan)
            dr, dl, b = mcu.read()
            robot.predict(dr, dl, b)
            robot.correct()
            robot.add_waypoint()
        time.sleep(0.001)
except KeyboardInterrupt:
    lidar.stop()
    mcu.stop()
    robot.save_data()