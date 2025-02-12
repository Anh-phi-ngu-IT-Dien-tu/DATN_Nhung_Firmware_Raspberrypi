from feature_extraction import FeatureExtraction
import numpy as np
import math
import json

class EkfSlam(FeatureExtraction):
    def __init__(self, min_range, max_range, point_dist_threshold, min_cluster_size, max_cluster_size,
                 avg_angles_lower_bound, avg_angles_upper_bound, std_angles_threshold, min_radius, max_radius,
                 max_landmarks, Q, R, maha_threshold, waypoint_min_distance):
        super().__init__(min_range, max_range, point_dist_threshold, min_cluster_size, max_cluster_size,
                         avg_angles_lower_bound, avg_angles_upper_bound, std_angles_threshold, min_radius, max_radius)
        
        # Max number of landmarks
        self.max_lm = max_landmarks

        # Number of known landmarks
        self.known_lm = 0

        # Initial state
        self.mean = np.zeros((2*max_landmarks + 3, 1))
        self.cov = np.zeros((2*max_landmarks + 3, 2*max_landmarks + 3))
        self.cov[0, 0] = 0**2
        self.cov[1, 1] = 0**2
        self.cov[2, 2] = np.deg2rad(0)**2
        for i in range(3, 2*max_landmarks + 3):
            self.cov[i, i] = 1e6

        # Noise matrix
        self.Q = Q
        self.R = R

        # Data association threshold
        self.maha_th = maha_threshold

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
        Gx = np.array(([[0, 0, -delta_y],
                        [0, 0, delta_x],
                        [0, 0, 0]]))

        # map Gx matrix (3x3) to (2N+3)x(2N+3) dimensional space
        Fx = np.eye(3, 2 * self.max_lm + 3)
        G = np.eye(2 * self.max_lm + 3) + Fx.T @ Gx @ Fx

        # predict robot's pose covariance
        self.cov = G @ self.cov @ G.T + Fx.T @ self.Q @ Fx

    # Call this method to correct robot's pose from lidar's measurements
    def correct(self):
        for landmark in self.landmarks:
            # This list stores the index of the closest landmark in database and the observed landmark
            lm_id = []
            
            # Convert observed landmark to world frame
            lmw = self.transform_global(landmark)

            # Temporarily add new observed landmark to database as new unobserved landmark
            self.mean[2*self.known_lm + 3, 0] = lmw[0, 0]
            self.mean[2*self.known_lm + 4, 0] = lmw[1, 0]
            
            # Find the closest landmark in database
            if self.known_lm > 0:
                distance = {}
                for i in range(self.known_lm):
                    distance[i] = math.sqrt((self.mean[2*i + 3, 0] - lmw[0, 0])**2 + (self.mean[2*i + 4, 0] - lmw[1, 0])**2)
                lm_id.append(min(distance, key=distance.get))

            # Add the obsereved landmark to list
            lm_id.append(self.known_lm)

            # This list stores the range and bearing of the landmarks
            z_list = []
            # This list stores the Jacobian matrix of the landmarks
            H_list = []
            # This list stores the inverse of the innovation covariance of the landmarks
            inv_psi_list = []

            for i in lm_id:
                lm_delta_x = self.mean[2*i + 3, 0] - self.mean[0, 0]
                lm_delta_y = self.mean[2*i + 4, 0] - self.mean[1, 0]
                q = lm_delta_x*lm_delta_x + lm_delta_y*lm_delta_y
                z = np.array([[math.sqrt(q)],
                              [math.atan2(lm_delta_y, lm_delta_x) - self.mean[2, 0]]])
                z_list.append(z)
                
                # Jacobian of measurement
                Hx = 1/q * np.array([[-np.sqrt(q) * lm_delta_x, -np.sqrt(q) * lm_delta_y, 0, np.sqrt(q) * lm_delta_x, np.sqrt(q) * lm_delta_y],
                                     [lm_delta_y, -lm_delta_x, -q, -lm_delta_y, lm_delta_x]])
                Fx = np.row_stack((np.eye(3, 2*self.max_lm + 3), np.eye(2, 2*self.max_lm + 3, 2*i + 3)))
                H = Hx @ Fx
                H_list.append(H)

                # Inverse of the innovation covariance
                inv_psi = np.linalg.inv(H @ self.cov @ H.T + self.R)
                inv_psi_list.append(inv_psi)

            if self.known_lm > 0:
                pi = ((z_list[1] - z_list[0]).T @ inv_psi_list[0] @ (z_list[1] - z_list[0]))[0, 0]
                if pi < self.maha_th:
                    j = 0
                else:
                    j = 1
                    self.known_lm += 1
            else:
                j = 0
                self.known_lm += 1

            K = self.cov @ H_list[j].T @ inv_psi_list[j]
            self.mean += K @ (z_list[-1] - z_list[j])
            self.cov = (np.eye(2*self.max_lm + 3) - K @ H_list[j]) @ self.cov

    def add_waypoint(self):
        if len(self.waypoints) == 0:
            self.waypoints.append((self.mean[0, 0], self.mean[1, 0]))
        else:
            d = math.sqrt((self.mean[0, 0] - self.waypoints[-1][0])**2 + (self.mean[1, 0] - self.waypoints[-1][1])**2)
            if d > self.waypoint_th:
                self.waypoints.append([self.mean[0, 0], self.mean[1, 0]])

    # Save landmarks and waypoints
    def save_data(self):
        saved_landmarks = []
        for i in range(self.known_lm):
            saved_landmarks.append([self.mean[2*i + 3, 0], self.mean[2*i + 4, 0]])
        with open("saved_landmarks.json", "w") as f:
            json.dump(saved_landmarks, f)

        with open("waypoints.json", "w") as f:
            json.dump(self.waypoints, f)