import paho.mqtt.client as mqtt

class NAO:
    def __init__(self):
        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(MQTT_HOST, MQTT_PORT)
        
        # Subscribe to XArm's MQTT topics
        self.client.subscribe("XARM/ball_grabbed")
        self.client.subscribe("XARM/player_lost")
        #self.client.subscribe("XARM/*")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("Failed to connect to MQTT broker")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker")

    def on_message(self, client, userdata, msg):
        if msg.topic == "XARM/ball_grabbed":
            # When XArm grabs a ball, NAO says "Ready player one"
            self.say("Ready player one")
        elif msg.topic == "XARM/player_lost":
            # When a player loses, NAO says "Oh no player 1 lost"
            self.say("Oh no player 1 lost")

    def say(self, message):
        # NAO sends a MQTT message to indicate its action
        self.client.publish(MQTT_TOPIC, message)


# Main function
if __name__ == "__main__":
    # Define MQTT host, port, and topic
    MQTT_HOST = "broker.emqx.io"
    MQTT_PORT = 1883
    MQTT_TOPIC = "NAO/SAY"
    
    # Initialize NAO
    nao = NAO()

    # Keep the program running to receive MQTT messages
    nao.client.loop_forever()
