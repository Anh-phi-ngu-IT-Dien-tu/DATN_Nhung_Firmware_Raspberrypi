import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from rplidar import RPLidar
from localization2 import Localization
import math

fig = plt.figure()
ax = fig.add_subplot(111)

lidar = RPLidar('COM10')
iterator = lidar.iter_scans(scan_type="express")

Q = np.diag([0.1*0.1, 0.1*0.1, math.pi/180*math.pi/180])
R = np.diag([120*120, math.pi/180*math.pi/180])

robot = Localization(min_range=150, max_range=2000, point_dist_threshold=10, min_cluster_size=10, max_cluster_size=40,
                     avg_angles_lower_bound=120*math.pi/180, avg_angles_upper_bound=160*math.pi/180, std_angles_threshold=8*math.pi/180,
                     min_radius=30, max_radius=40, Q=Q, R=R, linear_vel_max=10, turn_vel_max=5, maha_threshold=9, waypoint_range=50,
                     kp_dist=1, kp_heading=1, waypoint_min_distance=300)

def animate(i):
    scan = next(iterator)
    robot.extract_landmarks(scan)

    ax.clear()
    x = [val[0] for val in robot.landmarks]
    y = [val[1] for val in robot.landmarks]
    ax.scatter(x, y)
    ax.set_ylim([-1000, 1000])
    ax.set_xlim([-1000, 1000])

ani = animation.FuncAnimation(fig, animate, frames=100, interval=50)

plt.show()
lidar.stop()
lidar.disconnect()

print(robot.landmarks)