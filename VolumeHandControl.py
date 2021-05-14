import cv2
import time
import math
import numpy as np
import HandTrackingModule as ftm

# Defining parameters
wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

detector = ftm.HandDetector(detectionCon=0.7)

while True:
    ret, img = cap.read()
    img = detector.findHands(img)
    lmsList = detector.findPosition(img, draw=False)
    if len(lmsList) != 0:
        # print(lmsList[4],lmsList[8])
        x1,y1=lmsList[4][1],lmsList[4][2]
        x2, y2 = lmsList[8][1], lmsList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),7,(255,255,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx,cy), 7, (0, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)

        length=math.hypot(x2-x1,y2-y1)
        print(length)
        if length < 100:
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Checking Camera", img)
    cv2.waitKey(1)
