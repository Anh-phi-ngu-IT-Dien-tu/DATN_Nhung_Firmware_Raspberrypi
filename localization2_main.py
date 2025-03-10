from localization2 import Localization
from my_lidar import MyLidar
from my_mcu import MyMCU
import numpy as np
import time

lidar = MyLidar("/dev/ttyUSB1")
lidar.start()

mcu = MyMCU("/dev/ttyUSB0", 115200)
mcu.start()

# Noise parameters
Q = [0.8 , 0.8]
R = [0.01, np.deg2rad(1)]

robot = Localization(min_range=0, max_range=2000, point_dist_threshold=12, min_cluster_size=6, max_cluster_size=25,
                     avg_angles_lower_bound=np.deg2rad(120), avg_angles_upper_bound=np.deg2rad(160),
                     std_angles_threshold=np.deg2rad(6), min_radius=42, max_radius=47, Q=Q, R=R, maha_threshold=5.991,
                     linear_vel_max=50, turn_vel_max=np.deg2rad(30), waypoint_range=50, kp_dist=1, kp_heading=1,
                     waypoint_min_distance=25)

robot.load_landmarks()
robot.load_waypoints()

try:
    while True:
        time.sleep(0.05)
        dr, dl, b = mcu.read()
        robot.predict(dr, dl, b)
        scan = lidar.read()
        if len(scan) > 0:
            robot.extract_landmarks(scan)
            robot.correct()
            print(robot.test)
        robot.path_tracking()
        # print(robot.linear_vel, robot.turn_vel)
        mcu.write(robot.linear_vel, robot.turn_vel)
        
except KeyboardInterrupt:
    lidar.stop()
    mcu.write(0,0)
    mcu.stop()
    print(robot.mean)
    print(robot.cov)