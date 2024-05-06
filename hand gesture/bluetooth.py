import cv2
import mediapipe as mp
import keyboard
import time

# show thumb finger in right direction to switch on the bluetooth and same again second time for switching off the bluetooth. Or thumb finger in right direction to go to
# bluetooth button and thumbs up to switch off/on bluetooth.
# bluetooth network needs to be connected manually by selecting network name of your choice.
# Function to press right arrow key
def press_right():
    keyboard.press_and_release("right")
    print("Right arrow key pressed")

# Function to press Enter key
def press_enter():
    keyboard.press_and_release("enter")
    print("Enter key pressed")

# Function to press win + A key
def press_win_a():
    keyboard.press_and_release("win+a")
    print("Windows key + A pressed")

def main():
    # Add a delay of a few seconds before starting the main loop
    time.sleep(3)  # Adjust the delay time as needed

    # Press Windows key + A as soon as the camera starts
    press_win_a()

    # Initialize MediaPipe hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Flag to track whether Bluetooth is selected
    night_light_selected = False

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
                # Get the landmarks for index and thumb fingers
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Press right arrow key to move to Bluetooth option
                if not night_light_selected and index_tip.x < thumb_tip.x:
                    press_right()
                    night_light_selected = True

                # Check for thumbs-up gesture to press Enter key for Bluetooth
                if night_light_selected and thumb_tip.y < index_tip.y:
                    press_enter()

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
