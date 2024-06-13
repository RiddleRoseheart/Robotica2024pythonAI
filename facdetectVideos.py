import cv2
import mediapipe as mp
import time

class FaceDetector:
    def __init__(self, min_detection_confidence=0.3):
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
                    # Change the color of the bounding box to red
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    score = detection.score[0] * 100
                    cv2.putText(img, f'{score:.0f}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        return img

def main():
    # Specify the path to the video file
    video_path = 'securityCamVideos/202403011611.avi'
    cap = cv2.VideoCapture(video_path)
    detector = FaceDetector()
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Image", 800, 600)

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break # Break the loop if no more frames are available
        if len(img.shape) == 2:
            # Convert the grayscale image to color
            img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            img_color = img

        img_with_faces = detector.findFaces(img_color)

        cv2.imshow("Image", img_with_faces)
        # Increase the delay to slow down the video playback
        # For example, a delay of 1000 milliseconds (1 second) will slow down the video to half speed
        if cv2.waitKey(200) & 0xFF == ord('q'): # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()