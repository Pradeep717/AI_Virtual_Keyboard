# Importing the required libraries
import cv2
import numpy as np
import cvzone
from pynput.keyboard import Controller
import HandTrackerModule as htm
import time

wCam, hCam = 1280, 720 # width and height of the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

hand_detector = htm.handDetector(detectionCon=int(0.75))
keys = [ ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
         ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# create a keyboard object and define drawAll function
keyboard = Controller()
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0) # tr=0 means all corners are rounded 
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                    (255, 255, 255), 4)
    return img

# create a button class
class Button():
    def __init__(self, pos, text, size = [85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 20, 100 * i + 400], key))

finalText = ""

# main program for virtual keyboard
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = hand_detector.findHands(img)
    hands = hand_detector.findPosition(img,draw=False) # get the position of the hands
    handType = hand_detector.findHandsType()

    img = drawAll(img, buttonList)

    if hands and handType and len(hands) > 12:
        if 'Right' in handType:
            print('Right')
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < hands[4][1] < x + w and y < hands[4][2] < y + h: # check if the hand is on the button
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0,255, 255,), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                (255, 255, 255), 4)

                    l = hand_detector.findDistance(hands[4], hands[8], img, draw=False)



                    # when clicked
                    if l < 40:
                        keyboard.press(button.text)
                        # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4,
                                    (255, 255, 255), 4)

                        # wait for 0.3 seconds to avoid multiple key presses
                        time.sleep(0.3)
                        finalText += button.text

    cv2.rectangle(img, (45, 45), (960, 120), (175, 0, 175,), cv2.FILLED)
    cv2.putText(img, finalText, (60, 110), cv2.FONT_HERSHEY_PLAIN, 5,
                (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
