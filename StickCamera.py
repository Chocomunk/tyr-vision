#!/usr/bin/env python2
#
# StickCamera.py

import cv2

WIDTH = 640
HEIGHT = 480

try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)

try:
    # set resolution to 1080p
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
except: pass

try:
    # make the window resizable
    cv2.namedWindow("stick", cv2.cv.CV_WINDOW_NORMAL)
    cv2.resizeWindow("stick", WIDTH, HEIGHT)
except: pass


while cap.isOpened():
    ret, frame = cap.read()  # read a frame
    cv2.imshow('stick', frame)
    k = cv2.waitKey(1)
    if k == ord('q') or k == 27:  # exit with the 'q' or 'esc' key
        print "Exiting playback!"
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()
