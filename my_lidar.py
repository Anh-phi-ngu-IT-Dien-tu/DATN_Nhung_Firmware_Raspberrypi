from rplidar import RPLidar
import threading
import time

class MyLidar:
    def __init__(self, port):
        self.lidar = RPLidar(port)
        print(self.lidar.get_info())
        print(self.lidar.get_health())
        self.iterator = self.lidar.iter_scans(scan_type="express")
        self.thread = threading.Thread(target=self.update)
        self.lock = threading.Lock()
        self.data = []
        self.stopped = False

    def start(self):
        self.thread.start()

    def update(self):
        while True:
            if self.stopped:
                self.lidar.stop()
                self.lidar.stop_motor()
                self.lidar.disconnect()
                break
            scan = next(self.iterator)
            with self.lock:
                self.data = scan
            time.sleep(0.01)

    def read(self):
        with self.lock:
            scan = self.data
            self.data = []
        return scan
    
    def stop(self):
        self.stopped = True
        self.thread.join()