import cv2
import numpy as np
import pyautogui
import time

# Initialize variables for gesture recognition
tap_threshold = 1000  # Adjust the threshold as needed
gesture_detected = False
cooldown_duration = 2  # Adjust the cooldown duration as needed (in seconds)
last_detection_time = time.time()

# Main loop for capturing and processing video frames
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edges image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour = None

    if len(contours) > 0:
        # Find the largest contour (hand)
        contour = max(contours, key=cv2.contourArea)

        # Calculate the area of the hand contour
        hand_area = cv2.contourArea(contour)

        # Check for tap gesture based on area and cooldown
        current_time = time.time()
        if hand_area > tap_threshold and not gesture_detected and current_time - last_detection_time > cooldown_duration:
            pyautogui.hotkey('ctrl', 't')  # Simulate Windows button press to open a new tab in Chrome
            gesture_detected = True  # Set gesture detected state
            last_detection_time = current_time  # Update last detection time
        elif hand_area <= tap_threshold:
            gesture_detected = False  # Reset gesture detected state

    # Display the processed frame
    cv2.imshow('Closed Circle Gesture Detection', frame)

    # Check for 'q' key press to exit the loop
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
