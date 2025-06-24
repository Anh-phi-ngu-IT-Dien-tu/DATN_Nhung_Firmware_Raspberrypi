import paho.mqtt.client as mqtt
import threading
import time

class MyMQTT:
    def __init__(self, broker="test.mosquitto.org", topic="Robot"):
        self.broker = broker
        self.topic = topic
        self.client = mqtt.Client()
        self.thread = threading.Thread(target=self.do)
        self.x = 0
        self.y = 0
        self.theta = 0
        self.stopped = False

    def start(self):
        self.client.connect(self.broker)
        self.thread.start()

    def do(self):
        while True:
            time.sleep(1)
            if self.stopped:
                self.client.disconnect()
                break
            payload = f"{self.x:.0f}/{self.y:.0f}/{self.theta:.4f}"
            self.client.publish(self.topic, payload)

    def write(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def stop(self):
        self.stopped = True
        self.thread.join()