from robot_mqtt import Robot_MQTT_Position
import time

mqtt=Robot_MQTT_Position(host="broker.emqx.io")

mqtt.start_mqtt()

try: 
    while True:
        time.sleep(1)
        print(mqtt.message)

except KeyboardInterrupt:
    mqtt.stop_mqtt()