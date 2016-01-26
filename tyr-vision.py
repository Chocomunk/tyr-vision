#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#

from __future__ import division  # always use floating point division
import numpy as np
import cv2

#cap = cv2.VideoCapture(0)  # stream from webcam
#cap = cv2.VideoCapture('close-up-mini-U.mp4')  # https://goo.gl/photos/ECz2rhyqocxpJYQx9
cap = cv2.VideoCapture('mini-field.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6

while(cap.isOpened()):
    ret, frame = cap.read()  # read a frame
    if ret:
        # Find outlines of white objects
        white = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
        cv2.imshow('white threshold', white)  # show the threshold'ed image
        contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours in the thresholded image

        # Approximate outlines into polygons
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)  # smoothen the contours into simpler polygons
            # Filter through contours to detect a goal
            if cv2.contourArea(approx) > 1000 and len(approx) == 8:  # select contours with sufficient area and 8 vertices
                cv2.drawContours(frame, [approx], 0, (0,0,255), 5)  # draw the contour in red
                x,y,w,h = cv2.boundingRect(approx)  # find a non-rotated bounding rectangle
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)  # draw bounding rectangle in green
                if 1.2 < w/h < 1.8:  # filter by aspect ratio of the bounding box
                    cv2.drawContours(frame, [approx], 0, (255, 0, 255), 5)  # draw the contour in purple
                """
                # find the smallest bounding rectangle with rotation
                rect = cv2.minAreaRect(approx)
                box = cv2.cv.BoxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (255,0,0), 2)  # draw the rotated rectangle in blue
                """

        cv2.imshow('tyr-vision', frame)  # show the image output on-screen

        if cv2.waitKey(25) & 0xFF == ord('q'):  # exit with the 'q' key
            break
    else:
        break

cap.release()  # close the webcam interface
cv2.destroyAllWindows()  #LinuxWorldDomination

