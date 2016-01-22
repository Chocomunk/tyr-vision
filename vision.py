#!/usr/bin/env python2
#
# tyr-vision
# Team 8 Stronghold vision program
#

import numpy as np
import cv2

# cap = cv2.VideoCapture(0)  # video stream from webcam
cap = cv2.VideoCapture('flashlight-tylersjacket.mp4')  # video stream from an MP4 file
# download video file from: https://drive.google.com/open?id=0B3CtH7XCgLzOT0trdTlpc1c0UlE

while(cap.isOpened()):
    ret, frame = cap.read()  # read a frame
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert the image to greyscale
    edges = cv2.Canny(frame, 100, 200)
    color_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    #color_edges[:,:,0] = 0  # set Blue channel to zero
    color_edges[:,:,1] = 0  # set Green channel to zero

    overlay_img = cv2.addWeighted(frame, 0.7, color_edges, 0.3, 0)
    cv2.imshow('tyr-vision', overlay_img)  # show the image output on-screen

    if cv2.waitKey(1) & 0xFF == ord('q'):  # exit with the 'q' key
        break

cap.release()  # close the webcam interface
cv2.destroyAllWindows()  #LinuxWorldDomination

