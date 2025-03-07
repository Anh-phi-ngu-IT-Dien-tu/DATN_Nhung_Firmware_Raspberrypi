from feature_extraction import FeatureExtraction
from my_lidar import MyLidar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
fig = plt.figure()
ax = fig.add_subplot(111)

lidar = MyLidar("/dev/ttyUSB1")
lidar.start()

robot = FeatureExtraction(min_range=150, max_range=6000, point_dist_threshold=12, min_cluster_size=6, max_cluster_size=25,
                          avg_angles_lower_bound=np.deg2rad(120), avg_angles_upper_bound=np.deg2rad(160),
                          std_angles_threshold=np.deg2rad(6), min_radius=42, max_radius=47)

def animate(i):
    scan = lidar.read()
    
    if len(scan) > 0:
        robot.extract_landmarks(scan)
        ax.clear()
        x = [val[0] for val in robot.landmarks]
        y = [val[1] for val in robot.landmarks]
        ax.scatter(x, y)
        ax.set_ylim([-6000, 6000])
        ax.set_xlim([-6000, 6000])

ani = animation.FuncAnimation(fig, animate, frames=100, interval=200)

plt.show()
lidar.stop()

print(robot.landmarks)