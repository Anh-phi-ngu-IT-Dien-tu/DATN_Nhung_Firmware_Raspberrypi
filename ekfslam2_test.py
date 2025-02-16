from ekfslam2 import EkfSlam
import math
import numpy as np

Q = [0.1, 0.1]
R = [0.1, np.deg2rad(1)]

robot = EkfSlam(min_range=0, max_range=12000, point_dist_threshold=10, min_cluster_size=10, max_cluster_size=40,
                avg_angles_lower_bound=90*math.pi/180, avg_angles_upper_bound=135*math.pi/180, std_angles_threshold=8.6*math.pi/180,
                min_radius=30, max_radius=40, max_landmarks=3, Q=Q, R=R, waypoint_min_distance=300, maha_threshold=9)

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

# # extract_landmark test case: lidar_test.py

# # wrap_angle test case
# print("# wrap_angle test case:")
# print("Case 1", 59 <= robot.wrap_angle(60*math.pi/180)*180/math.pi <= 61)
# print("Case 2", -121 <= robot.wrap_angle(240*math.pi/180)*180/math.pi <= -119)

# # predict test case
# print("predict test case:")
# print(robot.mean)
# print(robot.cov)
# robot.predict(10,-10,10)
# print(robot.mean)
# print(robot.cov)

# correct test case
robot.mean[0, 0] = 10
robot.mean[1, 0] = 0
robot.mean[2, 0] = 0
print("correct test case:")
print(robot.mean)
print(robot.cov)
print(robot.known_lm)
print(" ")
# robot.landmarks = [[100,100]]
# robot.correct()
# print(robot.mean)
# print(robot.cov)
# print(robot.known_lm)
# print(" ")
# robot.landmarks = [[500,500]]
# robot.correct()
# print(robot.mean)
# print(robot.cov)
# print(robot.known_lm)
# print(" ")
robot.mean[3, 0] = 100
robot.mean[4, 0] = 100
robot.cov[3, 3] = 0
robot.cov[4, 4] = 0
robot.known_lm = 1
robot.landmarks = [[120,120]]
robot.correct()
print(robot.mean)
print(robot.cov)
print(robot.known_lm)
print(" ")
# robot.landmarks = [[520,520]]
# robot.correct()
# print(robot.mean)
# print(robot.cov)
# print(robot.known_lm)

# # transform_global test case
# print("# transform_global test case:")
# robot.mean[0, 0] = 1
# robot.mean[1, 0] = 1
# robot.mean[2, 0] = math.pi/2
# print(robot.transform_global([1,0]))
# print("Ground truth: (1,2)")

# # add_waypoint test case
# print("# add_waypoint test case:")
# robot.mean[0, 0] = 1
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 1", len(robot.waypoints) == 1)
# robot.mean[0, 0] = 10
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 2", len(robot.waypoints) == 1)
# robot.mean[0, 0] = 350
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 3", len(robot.waypoints) == 2)
# robot.mean[0, 0] = 0
# robot.mean[1, 0] = 0
# robot.mean[2, 0] = 0
# robot.add_waypoint()
# print("Case 4", len(robot.waypoints) == 3)

# # save_data test case:
# print("# save_data test case:")
# robot.save_data()