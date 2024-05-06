import cv2
import pygetwindow as gw
import pyautogui
import mediapipe as mp

# Initialize video capture
cam = cv2.VideoCapture(0)

# Initialize MediaPipe for head tracking
face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1, 
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Variables for scrolling based on head movement
scroll_threshold = 20  # Adjust the scroll threshold as needed

# variables for distance estimation
KNOWN_DISTANCE = 76.2  # centimeter
KNOWN_WIDTH = 14.3  # centimeter
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
fonts = cv2.FONT_HERSHEY_COMPLEX
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ref_distance_set = False
focal_length_found = 0

# Function to calculate focal length
def focal_length(measured_distance, real_width, width_in_rf_image):
    focal_length_value = (width_in_rf_image * measured_distance) / real_width
    return focal_length_value

# Function to estimate distance
def distance_finder(focal_length, real_face_width, face_width_in_frame):
    distance = (real_face_width * focal_length) / face_width_in_frame
    return distance

# Function to detect face and get width
def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), WHITE, 1)
        face_width = w
    return face_width

while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Resize the frame to improve performance
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    # Process the frame to detect landmarks
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks

    # Check if landmarks are detected
    if landmark_points:
        landmarks = landmark_points[0].landmark

        # Get the y-coordinates of the heads
        left_head_y = landmarks[159].y * frame.shape[0]
        right_head_y = landmarks[386].y * frame.shape[0]

        # Calculate the vertical movement of the heads
        head_movement = left_head_y - right_head_y

        # Scroll up or down based on head movement thresholds
        if head_movement < -scroll_threshold:
            pyautogui.scroll(50)  # Scroll up by 50 units (adjust as needed)
        elif head_movement > scroll_threshold:
            pyautogui.scroll(-50)  # Scroll down by 50 units (adjust as needed)

    # Calling face_data function
    face_width_in_frame = face_data(frame)

    if face_width_in_frame != 0:
        if not ref_distance_set:
            # Set up reference distance and focal length on the first face detection
            focal_length_found = focal_length(KNOWN_DISTANCE, KNOWN_WIDTH, face_width_in_frame)
            ref_distance_set = True

        distance = distance_finder(focal_length_found, KNOWN_WIDTH, face_width_in_frame)

        if(distance>=45 and distance<=60):
            # Get the active window
            active_window = gw.getActiveWindow()

            if active_window:
                # Maximize the active window
                active_window.maximize()
                print(f"Window '{active_window.title}' maximized.")
            else:
                print("No active window found.")
                
        if(distance>=35 and distance<=40):
           pyautogui.hotkey('ctrl', 'f')

        # Drawing text on the frame
        cv2.putText(frame, f"Distance: {round(distance, 2)} cm", (50, 50), fonts, 1, WHITE, 2)

    else:
        # If no face detected, display a message indicating no face detected
        cv2.putText(frame, "No Face Detected", (50, 50), fonts, 1, RED, 2)

    # Display the frame
    cv2.imshow('Head Movement Scrolling and Distance Estimation', frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the OpenCV windows
cam.release()
cv2.destroyAllWindows()