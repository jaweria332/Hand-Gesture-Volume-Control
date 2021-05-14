import cv2
import time
import math
import numpy as np
import HandTrackingModule as ftm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Defining parameters
wcam, hcam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0

detector = ftm.HandDetector(detectionCon=0.7)

# PyCaw Code
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    ret, img = cap.read()
    img = detector.findHands(img)
    lmsList = detector.findPosition(img, draw=False)
    if len(lmsList) != 0:
        # print(lmsList[4],lmsList[8])
        x1, y1 = lmsList[4][1], lmsList[4][2]
        x2, y2 = lmsList[8][1], lmsList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 7, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 7, (0, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range was from 50 - 300
        # Volume Range is -65 - 0
        vol = np.interp(length, [25, 375], [minVol, maxVol])
        volBar = np.interp(length, [25, 375], [400, 150])
        volPer = np.interp(length, [25, 375], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 100:
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)

    if volPer > 80:
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
    elif volPer < 80:
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'FPS:{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Checking Camera", img)
    cv2.waitKey(1)
