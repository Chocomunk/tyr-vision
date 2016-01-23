#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#

import numpy as np
import cv2

# cap = cv2.VideoCapture(0)  # video stream from webcam
cap = cv2.VideoCapture('flashlight-tylersjacket.mp4')  # video stream from an MP4 file
# download video file from: https://drive.google.com/open?id=0B3CtH7XCgLzOT0trdTlpc1c0UlE

while(cap.isOpened()):
    ret, frame = cap.read()  # read a frame
    if ret:
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert the image to greyscale

        white = cv2.inRange(frame, (245, 245, 245), (255, 255, 255))
        contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        img = np.zeros((720, 1280, 3), np.uint8)
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(approx)
            if area > 4000 and len(approx) == 4:
                cv2.drawContours(img, [approx], 0, (0, 0, 255), 5)
        
        cv2.imshow('tyr-vision', img)  # show the image output on-screen

        if cv2.waitKey(25) & 0xFF == ord('q'):  # exit with the 'q' key
            break
    else:
        break

cap.release()  # close the webcam interface
cv2.destroyAllWindows()  #LinuxWorldDomination

