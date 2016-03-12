#!/usr/bin/env python2
#
# StickCamera.py

import time
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

video_writer = None
try:
    filename = time.strftime("%Y-%m-%d_%H-%M-%S.avi")
    CODEC = 1196444237
    FRAMERATE = 30
    video_writer = cv2.VideoWriter(filename, CODEC, FRAMERATE, (WIDTH, HEIGHT))
    print "Writing to video file %s" % filename
except:
    print "Failed to write video file!"


while cap.isOpened():
    ret, frame = cap.read()  # read a frame
    cv2.imshow('stick', frame)
    try:
        video_writer.write(frame)
    except:
        print "Couldn't write frame!"

    k = cv2.waitKey(1)
    if k == ord('q') or k == 27:  # exit with the 'q' or 'esc' key
        print "Exiting playback!"
        break


# Cleanup
cap.release()
cv2.destroyAllWindows()
