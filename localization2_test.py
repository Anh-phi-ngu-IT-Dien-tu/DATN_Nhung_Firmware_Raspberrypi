from localization2 import Localization
import math
import numpy as np

Q = [0.1, 0.1]
R = [0.1, np.deg2rad(1)]

robot = Localization(min_range=0, max_range=12000, point_dist_threshold=10, min_cluster_size=10, max_cluster_size=40, avg_angles_lower_bound=90*math.pi/180,
                     avg_angles_upper_bound=135*math.pi/180, std_angles_threshold=8.6*math.pi/180, min_radius=30, max_radius=40,
                     Q=Q, R=R, linear_vel_max=10, turn_vel_max=5, maha_threshold=9, waypoint_range=50, kp_dist=1, kp_heading=1,
                     waypoint_min_distance=100)

# # is_same_cluster test case
# point1 = (10,0)
# point2 = (30,math.pi/6)
# point3 = (100,0)
# point4 = (120,math.pi/6)
# print("# is_same_cluster test case:")
# print("Case 1", robot.is_same_cluster(point1, point2) == False)
# print("Case 2", robot.is_same_cluster(point3, point4) == True)

# # is_circle test case
# cluster1 = [(1,0),(1,math.pi/4),(1,math.pi/2),(1,3*math.pi/4)]
# cluster2 = [(2,math.pi/6),(1.1547,math.pi/3),(1,math.pi/2),(1.1547,2*math.pi/3),(2,5*math.pi/6)]
# print("# is_circle test case:")
# print("Case 1", robot.is_circle(cluster1) == False)
# print("Case 2", robot.is_circle(cluster2) == False)

# # fit_cicle test case
# cluster = [(1,0),(1,math.pi/4),(1,math.pi/2),(1,3*math.pi/4)]
# x, y, r = robot.fit_circle(cluster)
# print("# fit_circle test case:")
# print("x", 0<=x<=0.001)
# print("y", 0<=y<=0.001)
# print("r", 0.999<=r<=1.001)

# load_data test case
print("# load_data test case:")
print(robot.saved_landmarks)
print(robot.saved_waypoints)
robot.load_landmarks()
robot.load_waypoints()
print(robot.saved_landmarks)
print(robot.saved_waypoints)

# # predict test case
# print("# predict test case:")
# print(robot.mean)
# print(robot.cov)
# robot.predict(10, -10, 10)
# print(robot.mean)
# print(robot.cov)

# correct test case
robot.mean[0, 0] = 10
robot.mean[1, 0] = 0
robot.mean[2, 0] = 0
print("# correct test case:")
print(robot.mean)
print(robot.cov)
print(" ")
robot.landmarks = [[120,120]]
robot.correct()
print(robot.mean)
print(robot.cov)
print(" ")

# # transform_global test case
# print("# transform_global test case:")
# robot.mean[0, 0] = 1
# robot.mean[1, 0] = 1
# robot.mean[2, 0] = math.pi/2
# print(robot.transform_global([1,0]))
# print("Ground truth: (1,2)")

# # add_waypoint test case
# print("# add_waypoint test case:")
# robot.mean[0, 0] = 2
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 1", len(robot.waypoints) == 1)
# robot.mean[0, 0] = 10
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 2", len(robot.waypoints) == 1)
# robot.mean[0, 0] = 300
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 3", len(robot.waypoints) == 2)
# robot.mean[0, 0] = 0
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 4", len(robot.waypoints) == 3)

# # save_waypoints test case
# print("# save_waypoints test case:")
# robot.save_waypoints()

# # load_landmarks test case
# print("# load_landmarks test case:")
# robot.load_landmarks()
# print(robot.saved_landmarks)

# # load_waypoints test case
# print("# load_waypoints test case:")
# robot.load_waypoints()
# print(robot.saved_waypoints)

# # path_tracking test case
# robot.mean[0, 0] = 0
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# print("# path_tracking test case:")
# print(robot.last_waypoint_index)
# robot.path_tracking()
# print("Last waypoint index: ", robot.last_waypoint_index)
# print("Robot's linear velocity: ", robot.linear_vel)
# print("Robot's turn velocity: ", robot.turn_vel)
# robot.path_tracking()
# print("Last waypoint index: ", robot.last_waypoint_index)
# print("Robot's linear velocity: ", robot.linear_vel)
# print("Robot's turn velocity: ", robot.turn_vel)
# robot.mean[0, 0] = 280
# robot.mean[1, 0] = 0
# robot.path_tracking()
# print("Last waypoint index: ", robot.last_waypoint_index)
# print("Robot's linear velocity: ", robot.linear_vel)
# print("Robot's turn velocity: ", robot.turn_vel)
# robot.mean[0, 0] = 50
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 3*math.pi/4
# robot.path_tracking()
# print("Last waypoint index: ", robot.last_waypoint_index)
# print("Robot's linear velocity: ", robot.linear_vel)
# print("Robot's turn velocity: ", robot.turn_vel)