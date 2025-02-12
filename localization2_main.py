from localization2 import Localization
from my_lidar import MyLidar
from my_mcu import MyMCU
import math
import numpy as np
import time

# def bluetooth_handler():
#     bluetooth = serial.Serial("COM4", 115200)
#     while True:
#         data = bluetooth.read().decode()
#         if data == "f":
#             mcu.write(10, 0)
#         elif data == "l":
#             mcu.write(-5, 5)
#         elif data == "r":
#             mcu.write(5, -5)
#         else:
#             mcu.write(0, 0)

# bluetooth_thread = threading.Thread(target=bluetooth_handler, daemon=True)
# bluetooth_thread.start()

lidar = MyLidar("COM10")
lidar.start()

mcu = MyMCU("COM3", 115200)
mcu.start()

# Noise matrix
Q = np.diag([0.1**2, 0.1**2, np.deg2rad(1)**2])
R = np.diag([50**2, np.deg2rad(1)**2])

robot = Localization(min_range=0, max_range=4000, point_dist_threshold=10, min_cluster_size=10, max_cluster_size=40,
                     avg_angles_lower_bound=np.deg2rad(90), avg_angles_upper_bound=np.deg2rad(135),
                     std_angles_threshold=np.deg2rad(8.6), min_radius=30, max_radius=40, Q=Q, R=R, maha_threshold=9,
                     linear_vel_max=10, turn_vel_max=5, waypoint_range=50, kp_dist=1, kp_heading=1,
                     waypoint_min_distance=300)

robot.load_landmarks()
robot.load_waypoints()

try:
    while True:
        scan = lidar.read()
        if len(scan) > 0:
            robot.extract_landmarks(scan)
            d, alpha = mcu.read()
            if d != 0 or alpha != 0:
                delta_x = d * math.cos(robot.mean[2, 0] + alpha/2)
                delta_y = d * math.sin(robot.mean[2, 0] + alpha/2)
                robot.predict(delta_x, delta_y, alpha)
            robot.correct()
            # robot.add_waypoint()
            robot.path_tracking()
            mcu.write(robot.linear_vel, robot.turn_vel)
        time.sleep(0.001)
except KeyboardInterrupt:
    lidar.stop()
    mcu.stop()
    # robot.save_waypoints()