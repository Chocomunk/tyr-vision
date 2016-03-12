#!/usr/bin/env python2
#
# StickCamera.py
#

# LIBRARY IMPORTS
import cv2

# LOCAL MODULE IMPORTS
import videooutput

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

try:
    cap = cv2.VideoCapture(0)
    print "Opened camera 0"
except:
    cap = cv2.VideoCapture(1)
    print "Opened camera 1"

try:
    # set resolution to 1080p
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
except:
    print "Failed to set camera resolution to %sx%s!" % (CAMERA_WIDTH, CAMERA_HEIGHT)


try:
    # make the window resizable
    cv2.namedWindow("stick", cv2.cv.CV_WINDOW_NORMAL)
    cv2.resizeWindow("stick", WINDOW_WIDTH, WINDOW_HEIGHT)
except:
    print "Failed to set window size!"


while cap.isOpened():
    ret, frame = cap.read()  # read a frame
    cv2.imshow('stick', frame) # show on screen
    k = cv2.waitKey(1)
    if k == ord('q') or k == 27:  # exit with the 'q' or 'esc' key
        print "Exiting playback!"
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()
