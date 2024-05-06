import cv2
import mediapipe as mp
import pyautogui

def play_next_video():
    pyautogui.hotkey('shift', 'n')

def play_previous_video():
    pyautogui.hotkey('shift', 'p')

def detect_gesture(frame, landmarks):
    # Detect the middle finger gesture for next and previous video
    right_middle_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    left_middle_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP - 5]
    
    right_wrist_y = landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y
    left_wrist_y = landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST - 5].y

    # Check if the right middle finger is pointing upwards for next video
    if right_middle_tip.y < right_wrist_y:
        play_next_video()

    # Check if the left middle finger is pointing upwards for previous video
    if left_middle_tip.y < left_wrist_y:
        play_previous_video()

def gesture_command():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                detect_gesture(frame, landmarks)

        cv2.imshow('Gesture Detection for Video Control', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_command()
