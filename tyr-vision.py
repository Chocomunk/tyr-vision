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

# Load reference U shape and extract its contour
goal_img = cv2.imread('goal.png', 0)
goal_contours, hierarchy = cv2.findContours(goal_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
goal_contour = goal_contours[0]

# Video options
show_video = True
save_video = False

# Video dimensions
frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

# Variables needed for saving the video
if save_video:
    filename = time.strftime("%Y-%m-%d_%H:%M:%S.avi")
    video_writer = cv2.VideoWriter(filename, cv2.cv.CV_FOURCC("M", "J", "P", "G"), 15, (frame_width, frame_height))

def find_best_match(contours):
    # Approximate outlines into polygons
    best_match = None # Stores best matching contour for U shape
    best_match_similarity = 1000 # Similarity of said contour to expected U shape
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)  # smoothen the contours into simpler polygons
        # Filter through contours to detect a goal
        if cv2.contourArea(approx) > 1000 and len(approx) == 8:  # select contours with sufficient area and 8 vertices
            cv2.drawContours(frame, [approx], 0, (0,0,255), 2)  # draw the contour in red
            # test to see if this contour is the best match
            similarity = cv2.matchShapes(approx, goal_contour, 3, 0)
            if similarity < best_match_similarity and similarity < 0.8: # Record contour most similar to U shape
                best_match_similarity = similarity
                best_match = approx
    return best_match

# Draw match information on img
def display_match(match, img):
    cv2.drawContours(img, [match], 0, (255, 255, 0), 3) # Draw best match for U shape in cyan
    x,y,w,h = cv2.boundingRect(match)  # find a non-rotated bounding rectangle
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)  # draw bounding rectangle in green

    # Draw goal contour based on the bounding box
    tape_x = int(w/10)
    tape_y = int(h/7)
    goal_x = x+tape_x
    goal_y = y-h+tape_y
    goal_w = int(w*4/5)
    goal_h = int(h*12/7)
    cv2.rectangle(img, (goal_x, goal_y), (goal_x+goal_w, goal_y+goal_h), (255,0,255), 2)  # draw the goal bounding box in purple
    # circle parameters
    radius = int(goal_w/2)
    center = (goal_x+radius, goal_y+radius)
    cv2.circle(img, center, radius, (0,255,255), 2)
    # Display center point and lines
    center_x, center_y = match_center(best_match)
    cv2.circle(frame, (center_x, center_y), 1, (0, 128, 255), 2) # Center point in orange
    cv2.line(frame, (center_x, 0), (center_x, frame_height), (255, 128, 0), 2) # Vertical line through center in dark blue

def match_center(match):
    x, y, w, h = cv2.boundingRect(match)
    return int(x + w/2), y

while(cap.isOpened()):
    pause = False
    ret, frame = cap.read()  # read a frame
    if ret:
        # Find outlines of white objects
        white = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))
        contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours in the thresholded image

        best_match = find_best_match(contours)

        cv2.rectangle(frame, (0, 0), (320, 48), (0, 0, 0), -1) # Rectangle where text will be displayed
        if best_match is None:
            cv2.putText(frame, "No match", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            #pause = True
        else:  # draw the best match and its bounding box
            display_match(best_match, frame)
            center_x, center_y = match_center(best_match)
            difference = center_x - int(frame_width / 2)
            if difference >= 0:
                text = "%dpx to right" % (difference)
            else:
                text = "%dpx to left" % (-difference)
            cv2.putText(frame, "%s" % text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))

        cv2.line(frame, (int(frame_width / 2), 0), (int(frame_width / 2), frame_height), (0, 0, 0), 2) # Vertical line through center of video (black)

        if show_video:
            cv2.imshow('tyr-vision', frame)  # show the image output on-screen
            if save_video:
                video_writer.write(frame)

        k = cv2.waitKey(25)  # wait 25ms for a keystroke
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
    else: # Close program when video ends
        break

cap.release()  # close the video interface
cv2.destroyAllWindows()  #LinuxWorldDomination

