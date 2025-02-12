import serial
import threading
import math
import struct
import time

class MyMCU:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(1)
        self.thread = threading.Thread(target=self.update)
        self.lock = threading.Lock()
        self.x = 0
        self.y = 0
        self.theta = 0
        self.stopped = False

    def start(self):
        self.thread.start()

    def update(self):
        while True:
            if self.stopped:
                self.ser.close()
                break
            try:
                buffer = self.ser.read(8)
                d, alpha = struct.unpack('ff', buffer)
                with self.lock:
                    self.x += d * math.cos(self.theta + alpha/2)
                    self.y += d * math.sin(self.theta + alpha/2)
                    self.theta += alpha
            except:
                pass

    def read(self):
        with self.lock:
            d = math.sqrt(self.x**2 + self.y**2)
            alpha = self.theta
            self.x = 0
            self.y = 0
            self.theta = 0
        return d, alpha
    
    def write(self, linear_vel, turn_vel):
        buffer = struct.pack('ff', linear_vel, turn_vel)
        self.ser.write(buffer)

    def stop(self):
        self.stopped = True
        self.thread.join()