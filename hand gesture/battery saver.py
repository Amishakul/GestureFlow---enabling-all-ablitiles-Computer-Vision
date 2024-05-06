import cv2
import mediapipe as mp
import keyboard
import time

#show down thumbs down finger to turn on battery saver and thumbs down again second time to switch battery saver off. Or thumbs down to go to
#battery saver button and thumbs up to switch off/on battery.

# Function to press down arrow key
def press_down():
    keyboard.press_and_release("down")
    print("Down arrow key pressed")

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

    # Flag to track whether Battery Saver is selected
    battery_saver_selected = False

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

                # Press down arrow key to move to Battery Saver option
                if not battery_saver_selected and thumb_tip.y > index_tip.y:
                    press_down()
                    battery_saver_selected = True

                # Check for right key press to confirm Battery Saver selection
                if battery_saver_selected and keyboard.is_pressed("right"):
                    print("Battery Saver selected")

                # Check for thumbs-up gesture to press Enter key for Battery Saver
                if battery_saver_selected and thumb_tip.y < index_tip.y:
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
