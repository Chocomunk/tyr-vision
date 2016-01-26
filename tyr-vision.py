#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#

import numpy as np
import cv2

# cap = cv2.VideoCapture(0)  # video stream from webcam
#cap = cv2.VideoCapture('flashlight-tylersjacket.mp4')  # video stream from an MP4 file
cap = cv2.VideoCapture('close-up-mini-U.mp4')  # https://goo.gl/photos/ECz2rhyqocxpJYQx9
#cap = cv2.VideoCapture('mini-field.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6

while(cap.isOpened()):
    ret, frame = cap.read()  # read a frame
    if ret:
        # Find outlines of white objects
        white = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
        cv2.imshow('white threshold', white)
        contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        img = np.zeros((720, 1280, 3), np.uint8)
        # Approximate outlines into polygons
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            # Only draw outlines of large rectangles
            if cv2.contourArea(approx) > 1000 and len(approx) == 8:
                cv2.drawContours(frame, [approx], 0, (0, 0, 255), 5)  # draw the contour in red
                x,y,w,h = cv2.boundingRect(approx)  # find a non-rotated bounding rectangle
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)  # draw boudning rectangle in green
                # find the smallest bounding rectangle with rotation
                rect = cv2.minAreaRect(approx)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (255,0,0), 2)  # draw the rotated rectangle in blue

        cv2.imshow('tyr-vision', frame)  # show the image output on-screen

        if cv2.waitKey(25) & 0xFF == ord('q'):  # exit with the 'q' key
            break
    else:
        break

cap.release()  # close the webcam interface
cv2.destroyAllWindows()  #LinuxWorldDomination

