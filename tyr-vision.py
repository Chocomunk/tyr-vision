#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#

from __future__ import division  # always use floating point division
import numpy as np
import cv2
import time

#cap = cv2.VideoCapture(0)  # stream from webcam
#cap = cv2.VideoCapture('close-up-mini-U.mp4')  # https://goo.gl/photos/ECz2rhyqocxpJYQx9
cap = cv2.VideoCapture('mini-field.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6

# Load expected U shape and extract contour
goal_img = cv2.imread('goal.png', 0)
goal_contours, hierarchy = cv2.findContours(goal_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
goal_contour = goal_contours[0]

# Whether or not to show the video and to save the video
show_video = True
save_video = False

# Variables needed for saving the video
if save_video:
    frame_width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    filename = time.strftime("%Y-%m-%d_%H:%M:%S.avi")
    video_writer = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC("M", "J", "P", "G"), 15, (int(frame_width), int(frame_height)))

while(cap.isOpened()):
    pause = False
    ret, frame = cap.read()  # read a frame
    if ret:
        # Find outlines of white objects
        white = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
        if show_video:
            cv2.imshow('white threshold', white)  # show the threshold'ed image
        contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours in the thresholded image

        # Approximate outlines into polygons
        best_match = None # Stores best matching contour for U shape
        best_match_similarity = 1000 # Similarity of said contour to expected U shape
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)  # smoothen the contours into simpler polygons
            # Filter through contours to detect a goal
            if cv2.contourArea(approx) > 1000 and len(approx) == 8:  # select contours with sufficient area and 8 vertices
                cv2.drawContours(frame, [approx], 0, (0,0,255), 5)  # draw the contour in red
                x,y,w,h = cv2.boundingRect(approx)  # find a non-rotated bounding rectangle
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)  # draw bounding rectangle in green
                similarity = cv2.matchShapes(approx, goal_contour, 3, 0)
                if similarity < best_match_similarity and similarity < 0.8: # Record contour most similar to U shape
                    best_match_similarity = similarity
                    best_match = approx

        if best_match is None:
            print "No match"
            #pause = True
        else:
            cv2.drawContours(frame, [best_match], 0, (255, 255, 0), 6) # Draw best match for U shape

        if show_video:
            cv2.imshow('tyr-vision', frame)  # show the image output on-screen
        if save_video:
            video_writer.write(frame)

        k = cv2.waitKey(1)  # wait 25ms for a keystroke
        if k == ord('q'):  # exit with the 'q' key
            print "Exiting playback!"
            break
        elif k == ord(' '):  # pause with the spacebar
            pause = True

        if pause:
            print "Pausing video"
            while True:
                if cv2.waitKey(25) == ord(' '):  # resume with the spacebar
                    print "Resuming video"
                    break

    else:
        break

cap.release()  # close the webcam interface
cv2.destroyAllWindows()  #LinuxWorldDomination

