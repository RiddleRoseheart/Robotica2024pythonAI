import cv2
import mediapipe as mp
import time
import math
import paho.mqtt.client as mqtt

# Global MQTT variables
MQTT_HOST = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "NAO/SAY"

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils

        # Initialization of MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.connect(MQTT_HOST, MQTT_PORT)

        # Initialization of last_published_time
        self.last_published_time = 0

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("Failed to connect to MQTT broker")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT broker")

    def findHands(self,img, draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handno=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand= self.results.multi_hand_landmarks[handno]

            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),7,(255,0,255),cv2.FILLED)

        return lmList

    def detectThumbGesture(self, lmList):
        # Check if landmarks list is not empty
        if len(lmList) != 0:
            # Get the coordinates of thumb landmarks (thumb tip and base)
            thumb_tip = lmList[4]  # Thumb tip landmark (id: 4)
            thumb_base = lmList[2]  # Thumb base landmark (id: 2)

            # Compare y-coordinates to determine if thumb is up or down
            if thumb_tip[2] < thumb_base[2]:
                return "Duim Omhoog"
            else:
                return "Duim Omlaag"
        else:
            return None

    def detectHandOpenClose(self, lmList):
        # Check if landmarks list is not empty
        if len(lmList) != 0:
            # Calculate the Euclidean distance between thumb tip and little finger tip landmarks
            thumb_tip = lmList[4]  # Thumb tip landmark (id: 4)
            pink_tip = lmList[20]  # Little finger tip landmark (id: 20)
            distance = math.sqrt((pink_tip[1] - thumb_tip[1])**2 + (pink_tip[2] - thumb_tip[2])**2)

            # Define a threshold distance to determine hand open or closed
            threshold_distance = 150  # Adjust this threshold as needed

            # Check if distance is larger than threshold to determine hand open or closed
            if distance > threshold_distance:
                return "Open"
            else:
                return "Gesloten"
        else:
            return None

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    # Initialize variables for tracking time
    last_gesture_time = time.time()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        thumb_gesture = detector.detectThumbGesture(lmList)
        hand_open_close = detector.detectHandOpenClose(lmList)

        gesture_to_publish = ""
        current_time = time.time()

        if thumb_gesture is not None and hand_open_close is not None:
            gesture_to_publish = f"{thumb_gesture} {hand_open_close}"
        elif thumb_gesture is not None:
            gesture_to_publish = thumb_gesture
        elif hand_open_close is not None:
            gesture_to_publish = hand_open_close

        # Check if there is a gesture to publish
        if gesture_to_publish:
            # Check if 2 seconds have passed since the last gesture
            if current_time - last_gesture_time > 5:
                detector.client.publish(MQTT_TOPIC, gesture_to_publish)
                last_gesture_time = current_time

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Afbeelding", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()

