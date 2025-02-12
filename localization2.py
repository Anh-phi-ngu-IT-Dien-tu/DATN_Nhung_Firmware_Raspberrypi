from feature_extraction import FeatureExtraction
import numpy as np
import math
import json

class Localization(FeatureExtraction):
    def __init__(self, min_range, max_range, point_dist_threshold, min_cluster_size, max_cluster_size,
                 avg_angles_lower_bound, avg_angles_upper_bound, std_angles_threshold, min_radius, max_radius,
                 Q, R, maha_threshold, linear_vel_max, turn_vel_max, waypoint_range, kp_dist, kp_heading,
                 waypoint_min_distance):
        super().__init__(min_range, max_range, point_dist_threshold, min_cluster_size, max_cluster_size,
                         avg_angles_lower_bound, avg_angles_upper_bound, std_angles_threshold, min_radius, max_radius)
        
        # Initial state
        self.mean = np.zeros((3,1))
        self.cov = np.diag([0**2, 0**2, np.deg2rad(0)**2])
        
        # Noise matrix
        self.Q = Q
        self.R = R

        # Known landmarks
        self.saved_landmarks = []

        # Data association threshold
        self.maha_th = maha_threshold

        # Path tracking
        self.saved_waypoints = []
        self.linear_vel_max = linear_vel_max
        self.turn_vel_max = turn_vel_max
        self.linear_vel = linear_vel_max
        self.turn_vel = 0
        self.last_waypoint_index = 0
        self.waypoint_range = waypoint_range
        self.kp_dist = kp_dist
        self.kp_heading = kp_heading

        # Create path
        self.waypoint_th = waypoint_min_distance
        self.waypoints = []

    # Return angle between -pi and pi
    def wrap_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))
    
    # Transform landmarks' coordinate in robot's frame to global frame
    def transform_global(self, point):
        pr = np.array([[point[0]],
                       [point[1]]])
        alpha = self.mean[2, 0]
        T = np.array([[self.mean[0, 0]],
                      [self.mean[1, 0]]])
        R = np.array([[math.cos(alpha), -math.sin(alpha)],
                      [math.sin(alpha), math.cos(alpha)]])
        return (R @ pr + T)
    
    # Call this method to update robot's pose base on odometry        
    def predict(self, delta_x, delta_y, delta_theta):
        # predict robot's pose mean
        self.mean[0, 0] += delta_x
        self.mean[1, 0] += delta_y
        self.mean[2, 0] = self.wrap_angle(self.mean[2, 0] + delta_theta)

        # Jacobian of the motion
        G = np.array(([[1, 0, -delta_y],
                       [0, 1, delta_x],
                       [0, 0, 1]]))

        # predict robot's pose covariance
        self.cov = G @ self.cov @ G.T + self.Q

    # Call this method to correct robot's pose from lidar's measurements
    def correct(self):
        for landmark in self.landmarks:
            lmw = self.transform_global(landmark)

            lm_delta_x_t = lmw[0, 0] - self.mean[0, 0]
            lm_delta_y_t = lmw[1, 0] - self.mean[1, 0]
            z_t = np.array([[math.sqrt(lm_delta_x_t**2 + lm_delta_y_t**2)],
                              [math.atan2(lm_delta_y_t, lm_delta_x_t) - self.mean[2, 0]]])

            distance = {}
            for i in range(len(self.saved_landmarks)):
                distance[i] = math.sqrt((self.saved_landmarks[i][0] - lmw[0, 0])**2 + (self.saved_landmarks[i][1] - lmw[1, 0])**2)
            closest_lm_index = min(distance, key=distance.get)

            lm_delta_x = self.saved_landmarks[closest_lm_index][0] - self.mean[0, 0]
            lm_delta_y = self.saved_landmarks[closest_lm_index][1] - self.mean[1, 0]
            q = lm_delta_x*lm_delta_x + lm_delta_y*lm_delta_y
            z = np.array([[math.sqrt(q)],
                          [math.atan2(lm_delta_y, lm_delta_x) - self.mean[2, 0]]])
            
            # Jacobian of measurement
            H = 1/q * np.array([[-np.sqrt(q) * lm_delta_x, -np.sqrt(q) * lm_delta_y, 0],
                                 [lm_delta_y, -lm_delta_x, -q]])

            # Inverse of the innovation covariance
            inv_psi = np.linalg.inv(H @ self.cov @ H.T + self.R)

            # Mahalanobis distance
            pi = ((z_t - z).T @ inv_psi @ (z_t - z))[0, 0]

            # Validation gate
            if pi < self.maha_th:
                K = self.cov @ H.T @ inv_psi
                self.mean += K @ (z_t - z)
                self.cov = (np.eye(3) - K @ H) @ self.cov
    
    def path_tracking(self):
        if self.last_waypoint_index < len(self.saved_waypoints):
            r = math.sqrt((self.saved_waypoints[self.last_waypoint_index][0] - self.mean[0, 0])**2 + (self.saved_waypoints[self.last_waypoint_index][1] - self.mean[1, 0])**2)
            if r < self.waypoint_range:
                self.last_waypoint_index += 1
                if self.last_waypoint_index == len(self.saved_waypoints):
                    self.linear_vel = 0
                    self.turn_vel = 0
                else:
                    self.pid_controller()
            else:
                self.pid_controller()
                
        else:
            self.linear_vel = 0
            self.turn_vel = 0

    def pid_controller(self):
        e_dist = math.sqrt((self.saved_waypoints[self.last_waypoint_index][0] - self.mean[0, 0])**2 + (self.saved_waypoints[self.last_waypoint_index][1] - self.mean[1, 0])**2)
        e_heading = self.wrap_angle(math.atan2(self.saved_waypoints[self.last_waypoint_index][1] - self.mean[1, 0], self.saved_waypoints[self.last_waypoint_index][0] - self.mean[0, 0]) - self.mean[2, 0])
        self.linear_vel = self.kp_dist * e_dist
        self.turn_vel = self.kp_heading * e_heading

        if self.linear_vel > self.linear_vel_max:
            self.linear_vel = self.linear_vel_max

        if self.turn_vel > self.turn_vel_max:
            self.turn_vel = self.turn_vel_max
        elif self.turn_vel < -self.turn_vel_max:
            self.turn_vel = -self.turn_vel_max

    def load_landmarks(self):
        with open("saved_landmarks.json", "r") as f:
            self.saved_landmarks = json.load(f)

    def load_waypoints(self):
        with open("waypoints.json", "r") as f:
            self.saved_waypoints = json.load(f)

    def add_waypoint(self):
        if len(self.waypoints) == 0:
            self.waypoints.append((self.mean[0, 0], self.mean[1, 0]))
        else:
            d = math.sqrt((self.mean[0, 0] - self.waypoints[-1][0])**2 + (self.mean[1, 0] - self.waypoints[-1][1])**2)
            if d > self.waypoint_th:
                self.waypoints.append([self.mean[0, 0], self.mean[1, 0]])

    # Save waypoints
    def save_waypoints(self):
        with open("waypoints.json", "w") as f:
            json.dump(self.waypoints, f)