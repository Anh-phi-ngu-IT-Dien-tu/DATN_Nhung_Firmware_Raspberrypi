import paho.mqtt.publish as publish
import threading

class Robot_MQTT:
    def __init__(self,hostname="test.mosquitto.org",topic="Robot",port=1883):
        self.hostname=hostname
        self.port=port
        self.topic=topic
        self.thread = threading.Thread(target=self.Send_through_MQTT)
        self.lock = threading.Lock()

    def Send_through_MQTT(self,message):
        publish.single(self.topic,message,self.hostname,self.port)

    def Start_Publisher(self):
        self.thread.start()

    def Stop_Publisher(self):
        self.thread.join()