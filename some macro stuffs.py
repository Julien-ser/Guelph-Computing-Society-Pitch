import cv2
#import streamlit as st
import mediapipe as mp
import face_mesh as h
import os
import numpy as np
from PIL import Image
import pyautogui
import time

detector = h.FaceMesh()


cap = cv2.VideoCapture(0)
'''def circle_crop(img, xc, yc, radius):

    # define circles
    radius1 = 25
    radius2 = 75

    # draw filled circles in white on black background as masks
    mask1 = np.zeros_like(img)
    mask = cv2.circle(mask1, (xc,yc), radius, (255,255,255), -1)

    # put mask into alpha channel of input
    result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask[:,:,0]
    return result'''

y1 = 0
y2 = 0
ty = 1
by = 0
my = 0
mode = 1

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.find_mesh(img, draw=False)

    lis = detector.get_pos(img)

    for item in lis:
        if item[0] == 0:
            y1 = item[2]
            cv2.circle(img, (item[1], item[2]), 5, (0,255,255), 1)
        if item[0] == 5:
            cv2.circle(img, (item[1], item[2]), 5, (0,255,255), 1)
            y2 = item[2]
        if item[0] == 152:
            by = item[2]
        if item[0] == 10:
            ty = item[2]
        if item[0] == 18:
            my = item[2]
    dist = abs(y1 - y2)
    mdist = abs(y1 - my)
    baseline = abs(by - ty)
    ratio = dist/baseline
    mr = mdist/baseline
    if mr >= 0.17:
        if mode == 1:
            mode = 0
        else:
            mode = 1
        time.sleep(0.5)
    if ratio >= 0.26:
        if mode == 1:
            pyautogui.hotkey('ctrl', 'tab')
        else:
            pyautogui.hotkey('alt', 'tab')
        time.sleep(0.5)
        dist = 0
    
    #cv2.imshow('Image', img)
    cv2.waitKey(1)
