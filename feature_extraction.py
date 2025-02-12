import numpy as np
import math
import statistics

class FeatureExtraction:
    def __init__(self, min_range, max_range, point_dist_threshold, min_cluster_size, max_cluster_size,
                 avg_angles_lower_bound, avg_angles_upper_bound, std_angles_threshold, min_radius, max_radius):
        self.min_range = min_range
        self.max_range = max_range
        self.dist_th = point_dist_threshold
        self.min_clust = min_cluster_size
        self.max_clust = max_cluster_size
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.avg_l = avg_angles_lower_bound
        self.avg_u = avg_angles_upper_bound
        self.std_th = std_angles_threshold
        self.landmarks = []

    # Check if cluster forms a circle
    def is_circle(self, cluster):
        start_point = cluster[0]
        end_point = cluster[-1]
        angles = []
        for current_point in cluster[1:-1]:
            r1 = current_point[0]

            delta_phi = abs(start_point[1] - current_point[1])
            r2 = start_point[0]
            d = math.sqrt(r1*r1 + r2*r2 - 2*r1*r2*math.cos(delta_phi)) # Law of cosine
            angle_temp = math.asin(math.sin(delta_phi) * r1 / d ) # Law of sine
            angle = delta_phi + angle_temp

            delta_phi = abs(end_point[1] - current_point[1])
            r2 = end_point[0]
            d = math.sqrt(r1*r1 + r2*r2 - 2*r1*r2*math.cos(delta_phi)) # Law of cosine
            angle_temp = math.asin(math.sin(delta_phi) * r1 / d ) # Law of sine
            angle += delta_phi + angle_temp

            angles.append(angle)
        
        avg = statistics.mean(angles)
        std = statistics.stdev(angles)

        if (self.avg_l <= avg <= self.avg_u) and (std <= self.std_th):
            return True
        else:
            return False
        
    # Check if 2 point belong in the same cluster
    def is_same_cluster(self, point_1, point_2):
        r1 = point_1[0]
        r2 = point_2[0]
        cos_delta = math.cos(point_1[1] - point_2[1])
        C1 = math.sqrt(2 * (1 - cos_delta))
        Dth = self.dist_th + C1 * min(r1, r2)
        D = math.sqrt(r1*r1 + r2*r2 - 2*r1*r2*cos_delta)

        if D < Dth:
            return True
        else:
            return False
        
    # Find circle parameters using Bullock's method
    def fit_circle(self, cluster):
        N = len(cluster)
        xs = np.array([[point[0] * math.cos(point[1])] for point in cluster])
        ys = np.array([[point[0] * math.sin(point[1])] for point in cluster])
        ax = np.mean(xs)
        ay = np.mean(ys)
        u = xs - ax
        v = ys - ay

        Suu = np.sum(u*u)
        Suv = np.sum(u*v)
        Svv = np.sum(v*v)
        Suuu = np.sum(u*u*u)
        Svvv = np.sum(v*v*v)
        Suvv = np.sum(u*v*v)
        Svuu = np.sum(v*u*u)

        g = 1/2 * (Suuu + Suvv)
        h = 1/2 * (Svvv + Svuu)
        den = Suu*Svv - Suv*Suv

        uc = (g*Svv - h*Suv)/den
        vc = (h*Suu - g*Suv)/den

        xc = uc + ax
        yc = vc + ay
        r = np.sqrt(uc*uc + vc*vc + (Suu + Svv)/N)

        return xc, yc, r
    
    # Call this method to extract landmarks
    def extract_landmarks(self, scan):
        self.landmarks = []
        # Convert degree to radian and filter points in certain range
        points = [(meas[2], -meas[1]*math.pi/180) for meas in scan if self.min_range <= meas[2] <= self.max_range]

        # Cluster points
        clusters = []
        current_cluster = []
        for current_point in points:
            if len(current_cluster) == 0:
                current_cluster.append(current_point)
            else:
                if self.is_same_cluster(current_cluster[-1], current_point):
                    current_cluster.append(current_point)
                else:
                    clusters.append(current_cluster)
                    current_cluster = [current_point]

        # If the fisrt point and last point are closed, merge the first and last clusters
        if len(clusters) > 1:
            if self.is_same_cluster(points[0], points[-1]):
                clusters[-1] += clusters[0]
                clusters.pop(0)

        # Classify circle/non circle and find the circle parameters      
        for current_cluster in clusters:
            if self.min_clust <= len(current_cluster) <= self.max_clust:
                if self.is_circle(current_cluster):
                    x, y, r = self.fit_circle(current_cluster)
                    if self.min_radius <= r <= self.max_radius:
                        self.landmarks.append((x,y))
