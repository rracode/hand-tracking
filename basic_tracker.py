import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()     # Can give parameters
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTIme = 0

while True:
    success, img = cap.read()
    height, width, channels = img.shape
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x*width), int(lm.y*height)
                print(id, cx, cy)
                if id==4:
                    cv2.circle(img, (cx,cy),8,(0,255,255),cv2.FILLED)
                elif id==8:
                    cv2.circle(img, (cx,cy),8,(255,255,0),cv2.FILLED)
                elif id==12:
                    cv2.circle(img, (cx,cy),8,(255,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # for x in range(width//2):
    #     img[:, x, :], img[:, width-1-x, :] = img[:, width-1-x, :], img[:, x, :]

    # 0 -> about X-axis (vertical)
    # 1 -> about Y-axis (horizontal)
    # -1 -> both axes (diagonal)

    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime

    cv2.putText(img, str(int(fps)), (width-50,30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0),2)
    cv2.putText(img, "Press Q to quit", (width-175,height-15), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255),1)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break