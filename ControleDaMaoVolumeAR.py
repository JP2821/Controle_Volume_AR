import cv2
import mediapipe as mp
import time
import math

class detectarMao():
    def __init__(self,mode=False, maxMaos=2, deteccao=0.5, trava=0.5):
        self.mode = mode
        self.maxMaos = maxMaos
        self.deteccao = deteccao
        self.trava = trava

        self.mpMaos = mp.solutions.hands
        self.maos = self.mpMaos.Hands(self.mode, self.maxMaos, self.deteccao, self.trava)
        self.mpDesenho = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20] #id da ponta de cada dedo

    def procurarMaos(self, img, desenho=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.resultado = self.maos.process(imgRGB)

        if self.resultado.multi_hand_landmarks:
            for maosLms in self.resultado.multi_hand_landmarks:
                if desenho:
                    self.mpDesenho.draw_landmarks(img, maosLms, self.mpMaos.HAND_CONNECTIONS)
        return img

    def acharPosicao(self, img, maoNao=0, desenho=True):
        xList = []
        yList = []
        lmList = []
        if self.resultado.multi_hand_landmarks:
            minhaMao = self.resultado.multi_hand_landmarks[maoNao]
            for id, lm in enumerate(minhaMao.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                lmList.append([id, cx, cy])
                if desenho:
                    cv2.circle(img, (cx,cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detectar = detectarMao()
    while True:
        sucess, img = cap.read()
        img = detectar.procurarMaos(img)
        lmList = detectar.acharPosicao(img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2. waitKey(1)

if __name__ == "__main__":
    main()
