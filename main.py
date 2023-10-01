import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

# width and height of camera window
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,700)

detector = HandDetector(detectionCon=1)

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

Finaltext = ""

keyword = Controller()

#with dark background
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]), 20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5)

    return img


# with transparent backgrounnd
# def drawAll(img, buttonList):
#     imgnew = np.zeros_like(img,np.uint8)
#     for button  in buttonList:
#         x,y=button.pos
#         cvzone.cornerRect(imgnew,(button.pos[0], button.pos[1], button.size[0],button.size[1]),20,rt=0)
#         cv2.rectangle(imgnew,button.pos,(x+button.size[0],y+button.size[1]),(255,0,255),cv2.FILLED)
#         cv2.putText(imgnew,button.text,(x+48,y+60),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
#
#         out = img.copy()
#         alpha = 0.5
#         mask = imgnew.astype(bool)
#         print(mask.shape)
#         out[mask]=cv2.addWeighted(img,alpha,imgnew,1-alpha,0)[mask]
#         return out




class Button():
    def __init__(self, pos, text, size =[85,85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img, (x-10,y-10), (x + w+7, y + h+7), (175, 0, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 5)
                l,_,_ = detector.findDistance(8,12,img,draw=False)
                print(l)
                # WHEN CLICKED 
                if l<38:
                    keyword.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255),5)

                    Finaltext += button.text
                    sleep(0.15)

    cv2.rectangle(img, (50,350), (700, 450), (175, 0, 0), cv2.FILLED)
    cv2.putText(img, Finaltext, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

