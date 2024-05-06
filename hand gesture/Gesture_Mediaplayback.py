import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

#variables : 
width, height = 1280, 720
gestureThreshold = 300 #if the value is below 300 then it means above my line then will say that detect the gesture.



#camera setup : 
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4,height)

#Hand Detector : 
detector = HandDetector(detectionCon=0.8, maxHands=1)


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)# 1 means horizontal 0 means vertical.
    hands, img = detector.findHands(img) #,flipType=False = this is the value that is being displayed on the hand image. 


    #WHEN WE APPLY THE GESTURES WE NEED TO MAKE SURE THAT IT IS ABOVE THE FACE. SO THAT NORMAL HAND MOTION DOES NOT HAVE ANY EFFECT.
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(0,255,0),10) # Align your camera such that this line is in the middle of this line.

    if hands:# get the landmarks of this hand and no of fingers that are up.
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        cx,cy = hand['center']
        print(fingers)

        if cy<=gestureThreshold: # if hand is at the heigth of the face then check gestues;

            # current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            # fps = int(cap.get(cv2.CAP_PROP_FPS))

            #gesture 1 : 
            if fingers == [1,0,0,0,0]: # THUMB THEN GO LEFT 10 SEC IN VIDEO.
                pyautogui.press('left')
                time.sleep(1) 
            elif fingers ==[0,0,0,0,1]: # LAST FINGER THEN GO 10 SEC AHEAD IN VIDEO.
                pyautogui.press('right')
                time.sleep(1) 
            elif fingers == [1,1,1,1,1]: # ALL FINGERS SHOWN THEN PAUSE/RESUME THE VIDEO
                pyautogui.press('space')
                time.sleep(1)
            elif fingers == [0,1,1,1,0]: # 3 FINGERS SHOWN MIDDEL ONE THEN INC THE VOULUME.
                pyautogui.press('up')
                time.sleep(1)
            elif fingers == [0,1,1,1,1]: # 4 FINGERS SHOWN THEN DEC THE VOL OF VIDEO WHICH IS PLAYING.
                pyautogui.press('down')
                time.sleep(1)
    
    cv2.imshow('Image',img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()