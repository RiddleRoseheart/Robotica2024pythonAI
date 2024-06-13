import cv2
import mediapipe as mp
import time

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        self.min_detection_confidence = min_detection_confidence
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detector = self.mp_face_detection.FaceDetection(self.min_detection_confidence)

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_detector.process(imgRGB)
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = img.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                if draw:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return img

def main():
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img = detector.findFaces(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
