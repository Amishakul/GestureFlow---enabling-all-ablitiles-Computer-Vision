# up fist close, down open all fingers

import cv2
import mediapipe as mp
import pyautogui

# Initialize hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open the webcam
cap = cv2.VideoCapture(0)

# Set up screen dimensions
screen_width, screen_height = pyautogui.size()
scroll_speed = 10

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract hand landmarks
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Get coordinates of thumb and index finger tips
            thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
            index_x, index_y = int(index_tip.x * screen_width), int(index_tip.y * screen_height)

            # Check if thumb is above the index finger (scroll up)
            if thumb_y < index_y:
                pyautogui.scroll(scroll_speed)
                cv2.putText(frame, "Scroll Up", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Check if thumb is below the index finger (scroll down)
            elif thumb_y > index_y:
                pyautogui.scroll(-scroll_speed)
                cv2.putText(frame, "Scroll Down", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow("Hand Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
