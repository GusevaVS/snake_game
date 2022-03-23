import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import random
from snake_game_constructor import SnakeGame


def run_game(cap, detector, game):
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.game_over = False
        game.score = 0


cap = cv2.VideoCapture(0) 
cap.set(3, 3000) 
cap.set(4, 2000) 
detector = HandDetector(detectionCon=0.8, maxHands=1)
game = SnakeGame('poo.png')
while True:
    run_game(cap, detector, game)

