import cv2
import mediapipe as mp
import subprocess
import keyboard
# show thumbs up finger to launch system settings panel then again show thumbs up to activate wifi(sometimes you have to show thumbs up again incase wifi doesn't get on in first attempt thumbs up) on and show again to deactivate wifi
# wifi will get automatically connected to default network.
# Function to toggle wifi mode on Windows
def toggle_airplane_mode_windows():
    try:
        subprocess.run(["netsh", "interface", "set", "interface", "name='Wi-Fi'", "admin=disable"])
        print("Wifi mode turned OFF/ON")
    except Exception as e:
        print(f"Error turning off/on wifi: {e}")

# Function to press Enter key
def press_enter():
    keyboard.press_and_release("enter")
    print("Enter key pressed")

def main():
    # Initialize MediaPipe hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize MediaPipe drawing utilities
    mp_drawing = mp.solutions.drawing_utils

    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Flag to track whether wifi is selected
    wifi_selected = False

    while cap.isOpened():
        ret, frame = cap.read()

        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe hands
        results = hands.process(rgb_frame)

        # Check if hand landmarks are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the landmarks for thumb and pinky finger
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                # Press Windows key + A to select wifi
                if not wifi_selected and thumb_tip.y < pinky_tip.y:
                    keyboard.press_and_release("win+a")
                    print("Windows key + A pressed")
                    wifi_selected = True

                # Check for right shift key press to select wifi
                if wifi_selected and keyboard.is_pressed("right shift"):
                    print("wifi selected")

                # Check for thumbs-up gesture to press Enter key
                if wifi_selected and thumb_tip.y < pinky_tip.y:
                    press_enter()

        # Draw landmarks on the frame
        if results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame
        cv2.imshow('Hand Gestures', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
