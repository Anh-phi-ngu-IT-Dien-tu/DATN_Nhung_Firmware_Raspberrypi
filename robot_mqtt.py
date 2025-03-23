import paho.mqtt.client as mqtt

class Robot_MQTT_Position:

    def __init__(self,host="test.mosquitto.org",port=1883,topic="Robot"):
        self.message=None
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(host=host,port=port)
        self.x=0.0
        self.y=0.0
        self.theta=0.0
        self.temp_message=None
        self.topic=topic
        pass

    def on_connect(self,client, userdata, flags, rc):
        print("Connected with result code "+str(rc)) 
        # Subscribing in on_connect() - if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # topic
        client.subscribe(self.topic)
        
    # The callback for when a PUBLISH message is received from the server.
    def on_message(self,client, userdata, msg):
        # Do something else
    
        self.message=str(msg.payload.decode("utf-8"))
        try:
            self.temp_message=self.message.split('/')
            self.x=float(self.temp_message[0])
            self.y=float(self.temp_message[1])
            self.theta=float(self.temp_message[2])
        except:
            pass

    
    def publish(self,topic="Robot",message=""):
        self.client.publish(topic, message)

    def start_mqtt(self):
        self.client.loop_start()

    def stop_mqtt(self):
        self.client.loop_stop()