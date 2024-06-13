import cv2
import numpy as np

# Global variables to store the previous position of the object
prev_x = None
prev_y = None

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range of yellow color in HSV
        lower_color = np.array([20, 100, 100])  # Lower bound for yellow color
        upper_color = np.array([30, 255, 255])  # Upper bound for yellow color

        # Create a mask for the yellow object
        mask = cv2.inRange(hsv, lower_color, upper_color)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour
        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            # Determine the bounding rectangle of the largest contour
            x, y, w, h = cv2.boundingRect(max_contour)
            # Extend the bounding box size
            x -= 10
            y -= 10
            w += 20
            h += 20
            # Draw a rectangle around the largest contour (yellow object)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)  # Yellow color rectangle

            # Check if previous position exists
            global prev_x, prev_y
            if prev_x is not None and prev_y is not None:
                # Check if current position is to the left or right of previous position
                if x < prev_x:
                    direction_text_x = "LEFT"
                elif x > prev_x:
                    direction_text_x = "RIGHT"
                else:
                    direction_text_x = ""

                # Check if current position is higher or lower than previous position
                if y < prev_y:
                    direction_text_y = "UP"
                elif y > prev_y:
                    direction_text_y = "DOWN"
                else:
                    direction_text_y = ""

                # Display direction text next to the object
                cv2.putText(frame, direction_text_x, (x + w + 10, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, direction_text_y, (x + w + 10, y + h // 2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Update previous position
            prev_x = x
            prev_y = y

        # Show the image with the tracked object
        cv2.imshow("Yellow Object Tracking", frame)

        # Wait for a key press and break the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
