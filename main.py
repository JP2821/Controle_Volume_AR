#######################################
#
# By: João Pedro Ribeiro da Silva Dias
#
########################################
import cv2
import time
import numpy as np
import ControleDaMao as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
pTime=0

detectar = htm.detectarMao(deteccao=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
altura_Do_Volume = volume.GetVolumeRange()
min_vol = altura_Do_Volume[0]
max_vol = altura_Do_Volume[1]

while True:
    sucess, img = cap.read()
    img = detectar.procurarMaos(img)
    lmList = detectar.acharPosicao(img, desenho=False)
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 255, 0), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)

        comprimento = math.hypot(x2-x1, y2-y1)
        #print(comprimento)

        vol = np.interp(comprimento, [50, 300], [min_vol, max_vol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if comprimento < 50:
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)



    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
