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
        self.dr = 0
        self.dl = 0
        self.b = 0
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
                dr, dl, b = struct.unpack('fff', buffer)
                with self.lock:
                    self.dr += dr
                    self.dl += dl
                    self.b = b
            except:
                pass

    def read(self):
        with self.lock:
            dr = self.dr
            dl = self.dl
            b = self.b
            self.dr = 0
            self.dl = 0
        return dr, dl, b
    
    def write(self, linear_vel, turn_vel):
        buffer = struct.pack('ff', linear_vel, turn_vel)
        self.ser.write(buffer)

    def stop(self):
        self.stopped = True
        self.thread.join()