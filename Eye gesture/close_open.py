import cv2
import numpy as np
import dlib
import pygetwindow as gw
from math import hypot


cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Gesture_Project\Eye gesture\shape_predictor_68_face_landmarks.dat")

def midpoint(p1,p2):
    return int((p1.x + p2.x)/2), int((p1.y+p2.y)/2)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:

        # LEFT EYE CLOSE TO MINIMIZE THE CURRENT WINDOW.
        x, y = face.left(),face.top()
        x1,y1 = face.right(),face.bottom()
        # cv2.rectangle(frame,(x,y),(x1,y1),(0,255,0),2)
        landmarks = predictor(gray, face)
        # x = landmarks.part(36).x
        # y = landmarks.part(36).y
        # cv2.circle(frame,(x,y),3,(0,0,255),2)
        left_point = (landmarks.part(36).x,landmarks.part(36).y)
        right_point = (landmarks.part(39).x,landmarks.part(39).y)
        center_top = midpoint(landmarks.part(37),landmarks.part(38))
        center_bottom = midpoint(landmarks.part(41),landmarks.part(40))

        hor_line = cv2.line(frame, left_point, right_point, (0,255,0),2)
        ver_line = cv2.line(frame,center_top,center_bottom,(0,255,0),2)

        hor_line_length = hypot((left_point[0]-right_point[0]),(left_point[1]-right_point[1]))
        ver_line_length = hypot((center_top[0]-center_bottom[0]),(center_top[1]-center_bottom[1]))

        left_close_ratio = hor_line_length/ver_line_length
        # print(hor_line_length/ver_line_length)
        # RIGHT EYE CLOSE TO CLOSE THE CURRENT WINDOW.
        left_point_of_right = (landmarks.part(42).x,landmarks.part(42).y)
        right_point_of_right = (landmarks.part(45).x,landmarks.part(45).y)
        center_top_of_right = midpoint(landmarks.part(43),landmarks.part(44))
        center_bottom_of_right = midpoint(landmarks.part(47),landmarks.part(46))

        hor_line_of_right = cv2.line(frame, left_point_of_right, right_point_of_right, (0,255,0),2)
        ver_line_of_right = cv2.line(frame,center_top_of_right,center_bottom_of_right,(0,255,0),2)

        hor_line_length_of_right = hypot((left_point_of_right[0]-right_point_of_right[0]),(left_point_of_right[1]-right_point_of_right[1]))
        ver_line_length_of_right = hypot((center_top_of_right[0]-center_bottom_of_right[0]),(center_top_of_right[1]-center_bottom_of_right[1]))

        right_close_ratio = hor_line_length_of_right/ver_line_length_of_right
        # print(hor_line_length_of_right/ver_line_length_of_right)

        if(left_close_ratio>5 and right_close_ratio<5):
            # Get the currently active window
            print("left eye closed.")
            active_window = gw.getActiveWindow()

            # Minimize the active window
            if active_window:
                active_window.minimize()
                print(f"Window '{active_window.title}' minimized.")
            else:
                print("No active window found.") 

        

        if(right_close_ratio>5 and left_close_ratio<5):
            # Get the currently active window
            active_window = gw.getActiveWindow()
            print("right eye close.")

            # Close the active window
            if active_window:
                active_window.close()
                print(f"Window '{active_window.title}' closed.")
            # else:
            #     print("No active window found.")
        

    cv2.imshow("frame",frame)

    key=cv2.waitKey(1)
    if(key==27):
        break

cap.release()
cv2.destroyAllWindows()


