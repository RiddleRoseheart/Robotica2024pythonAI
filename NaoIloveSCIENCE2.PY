import paho.mqtt.client as mqtt_client
import random
import time
from naoqi import ALProxy

# MQTT Broker Details
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# NAO Text-to-Speech Proxy
tts = ALProxy("ALTextToSpeech", "<IP of your robot>", 9559)

# Callback Functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    mttq_received = msg.payload.decode()
    if mttq_received == "xarm_puts_ball":
        tts.say("Player 1 is ready!")
    elif mttq_received == "xarm_takes_ball":
        tts.say("Oh no, Player 1 lost!")

# MQTT Client Setup
client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(broker, port)

# Start MQTT Loop
client.loop_start()

# Main Function
def main():
    # Your main function logic here
    pass

if __name__ == "__main__":
    main()
