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

""" Video Input Settings """
#cap = cv2.VideoCapture(0)  # stream from webcam
#cap = cv2.VideoCapture('close-up-mini-U.mp4')  # https://goo.gl/photos/ECz2rhyqocxpJYQx9
cap = cv2.VideoCapture('mini-field.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6

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


""" Reference Target Contour """
# Load reference U shape and extract its contour
goal_img = cv2.imread('goal.png', 0)
goal_contours, hierarchy = cv2.findContours(goal_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
goal_contour = goal_contours[0]


def find_best_match(frame):
    """
    This is essentially the goal detection function.

    Returns the contour that best matches the target shape.
    This is done by thresholding the image, extracting contours, approximating
    the contours as polygons. The polygonal contours are then filtered by
    vertice count and minimum area. Finally, the similarity of a contour is
    determined by the matchShapes() function, and the best_match variable is set
    if the similarity is lower than the prior similarity value.

    This function should not modify anything outside of its scope.
    """
    # Find outlines of white objects
    white = cv2.inRange(frame, (230, 230, 230), (255, 255, 255))  # threshold detection of white regions
    contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours in the thresholded image

    # Approximate outlines into polygons
    best_match = None # Variable to store best matching contour for U shape
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


def draw_target(frame, target):
    """ Draws the given target contour with extrapolated goal shape and
    targeting visuals onto the given image. """
    cv2.drawContours(frame, [target], 0, (255, 255, 0), 3) # Draw target in cyan
    x,y,w,h = cv2.boundingRect(target)  # find a non-rotated bounding rectangle
    cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)  # draw bounding rectangle in green

    """
    # Draw goal contour based on the bounding box
    tape_x = int(w/10)
    tape_y = int(h/7)
    goal_x = x+tape_x
    goal_y = y-h+tape_y
    goal_w = int(w*4/5)
    goal_h = int(h*12/7)
    cv2.rectangle(frame, (goal_x, goal_y), (goal_x+goal_w, goal_y+goal_h), (255,0,255), 2)  # draw the goal bounding box in purple
    # circle parameters
    radius = int(goal_w/2)
    center = (goal_x+radius, goal_y+radius)
    cv2.circle(frame, center, radius, (0,255,255), 2)
    """
    # Display center point and lines
    center_x, center_y = target_center(target)
    #cv2.circle(frame, (center_x, center_y), 1, (0, 128, 255), 2) # Draw target center point in orange
    cv2.line(frame, (0, center_y), (frame_width, center_y), (255, 128, 0), 2) # Horizontal line through target center in dark blue
    cv2.line(frame, (center_x, 0), (center_x, frame_height), (255, 128, 0), 2) # Vertical line through target center in dark blue


def target_center(target):
    """ Returns the center point of a given target contour """
    x, y, w, h = cv2.boundingRect(target)
    return int(x + w/2), y


def draw_base_HUD(frame):
    """ Draws horizontal and vertical lines through center of the given frame """
    cv2.line(frame, (int(frame_width / 2), 0), (int(frame_width / 2), frame_height), (0, 0, 0), 2) # Vertical line through center of video (black)
    cv2.line(frame, (0, int(frame_height/2)), (frame_width, int(frame_height/2)), (0, 0, 0), 2)


def draw_targeting_HUD(frame, target):
    """ Draws the target by calling draw_target(), as well as crosshair lines
    and a textbook showing the target's displacement. """
    cv2.rectangle(frame, (0, 0), (320, 48), (0, 0, 0), -1) # Rectangle where text will be displayed
    if target is None:
        cv2.putText(frame, "No match", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        #pause = True
    else:  # draw the best match and its bounding box
        draw_target(frame, target)
        center_x, center_y = target_center(target)
        difference = center_x - int(frame_width / 2)
        if difference >= 0:
            text = "%dpx to right" % (difference)
        else:
            text = "%dpx to left" % (-difference)

        cv2.putText(frame, "%s" % text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))


""" BEGIN video processing loop """
while(cap.isOpened()):
    pause = False
    ret, frame = cap.read()  # read a frame
    if ret:
        draw_base_HUD(frame)
        best_match = find_best_match(frame)
        draw_targeting_HUD(frame, best_match)

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


""" Program clean up """
cap.release()  # close the video interface
cv2.destroyAllWindows()  #LinuxWorldDomination

