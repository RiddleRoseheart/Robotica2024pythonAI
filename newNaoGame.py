import paho.mqtt.client as mqtt

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received: {message}")
    
    if "GRAB" in message:
        # X Arm grabs a ball, NAO sends a message
        client.publish("xarm/response", "Oh no player 1 lost")
    elif "READY" in message:
        # X Arm is ready, NAO sends a message
        client.publish("xarm/response", "Ready player one")

def main():
    client = mqtt.Client("NAO")
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect("broker.emqx.io", 1883, 60)

    # Subscribe to the topic where X Arm sends messages
    client.subscribe("xarm/messages")

    # Start the loop to process callbacks and messages
    client.loop_start()

    try:
        while True:
            pass # Keep the script running
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down.")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
