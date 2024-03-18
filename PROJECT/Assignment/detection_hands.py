import cv2 as cv 
import mediapipe as mp

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

success, img = cap.read()
imgRGB = cv.cvtColor(img,cv.COLOR_BGR2RGB)
results = hands.process(imgRGB)


if results.multi_hands_landmarks :
    for handLms in results.multi_hands_landmarks
        