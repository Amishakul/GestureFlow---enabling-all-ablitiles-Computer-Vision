import cv2
import mediapipe as mp
import pyautogui
import time

# Define a cooldown period (in seconds)
cooldown_period = 3 # Adjust this as needed

# Variables to keep track of the last time each action was performed
last_next_song_time = time.time()
last_previous_song_time = time.time()

def play_next_song():
    global last_next_song_time
    current_time = time.time()
    if current_time - last_next_song_time >= cooldown_period:
        pyautogui.hotkey('ctrl', 'f')
        last_next_song_time = current_time

def play_previous_song():
    global last_previous_song_time
    current_time = time.time()
    if current_time - last_previous_song_time >= cooldown_period:
        pyautogui.hotkey('ctrl', 'b')
        last_previous_song_time = current_time

def detect_gesture(frame, landmarks):
    # Detect the index finger gesture for next and previous song
    right_index_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    left_index_tip = landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP - 5]
    
    right_wrist_y = landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y
    left_wrist_y = landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST - 5].y

    # Check if the right index finger is pointing upwards for next song
    if right_index_tip.y < right_wrist_y:
        play_next_song()

    # Check if the left index finger is pointing upwards for previous song
    if left_index_tip.y < left_wrist_y:
        play_previous_song()

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

        cv2.imshow('Gesture Detection for Media Player Control', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    gesture_command()
