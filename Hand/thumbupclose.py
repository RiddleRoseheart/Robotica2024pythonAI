import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands)
        self.mpDraw = mp.solutions.drawing_utils

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
                #print (id,cx,cy)
                lmList.append([id,cx,cy])
                #if id == 4:
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
                return "Thumb Up"
            else:
                return "Thumb Down"
        else:
            return None

    def detectHandOpenClose(self, lmList):
        # Check if landmarks list is not empty
        if len(lmList) != 0:
            # Calculate the Euclidean distance between thumb tip and little finger tip landmarks
            thumb_tip = lmList[4]  # Thumb tip landmark (id: 4)
            little_tip = lmList[20]  # Little finger tip landmark (id: 20)
            distance = math.sqrt((little_tip[1] - thumb_tip[1])**2 + (little_tip[2] - thumb_tip[2])**2)

            # Define a threshold distance to determine hand open or closed
            threshold_distance = 150  # Adjust this threshold as needed

            # Check if distance is larger than threshold to determine hand open or closed
            if distance > threshold_distance:
                return "Open"
            else:
                return "Closed"
        else:
            return None

def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        thumb_gesture = detector.detectThumbGesture(lmList)
        hand_open_close = detector.detectHandOpenClose(lmList)

        gesture_to_display = ""
        if thumb_gesture is not None and hand_open_close is not None:
            gesture_to_display = f"{thumb_gesture} {hand_open_close}"
        elif thumb_gesture is not None:
            gesture_to_display = thumb_gesture
        elif hand_open_close is not None:
            gesture_to_display = hand_open_close

        # Display the detected gesture on the image
        cv2.putText(img, gesture_to_display, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
