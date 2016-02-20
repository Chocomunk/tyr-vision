#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#

"""
U-SHAPE REFERENCE

 -  6-5 <- 2" wide   2-1
 |  | |              | |
 |  | |              | |
 |  | |              | |
14" | |              | |
 |  | |              | |
 |  | 4--------------3 |
 -  7------------------0 (start)
    |------- 18"-------|
"""

from __future__ import division  # always use floating point division
import numpy as np
import cv2
import serial
import sys
import time


""" DEFAULT SETTINGS """
""" Serial Output """
#port = '/dev/ttyS0' # primary DB9 RS-232 port
#port = '/dev/ttyUSB0' # primary USB-serial port
port = '/dev/ttyTHS0'  # primary 1.8V UART on the Jetson
baudrate = 9600
#baudrate = 15200

""" Video Settings """
#cap = cv2.VideoCapture(0)  # stream from webcam
#cap = cv2.VideoCapture('video_in/mini-field.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6
cap = cv2.VideoCapture('video_in/12ft.mp4')
#cap = cv2.VideoCapture('video_in/3ft-no-lights.mp4')
show_video = False
save_video = False
codec = cv2.cv.CV_FOURCC("H", "2", "6", "4")



""" PROCESS COMMAND LINE FLAGS """
i = 1
while i < len(sys.argv):
    flag = sys.argv[i]
    if flag[:2] == "--":
        if flag == "--show":
            show_video = True
        elif flag == "--save":
            save_video = True
        elif flag == "--device":
            i += 1
            cap.release()  # close default stream before opening a new one
            try:
                # an integer X indicates the webcam address, ie. /dev/videoX
                cap = cv2.VideoCapture(int(sys.argv[i]))
                # set resolution manually
                # the Logitech C920 is 1080p
                cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
                cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
                print "Opened webcam at: /dev/video%s" % sys.argv[i]
            except:
                # if it's not an integer, it's a filepath for a video
                cap = cv2.VideoCapture("video_in/" + sys.argv[i])
                print "Opened video file at: %s" % sys.argv[i]
        elif flag == "--port":
            i += 1
            port = sys.argv[i]
        elif flag == "--baudrate":
            i += 1
            baudrate = sys.argv[i]
        elif flag == "--codec":
            i += 1
            codec = cv2.cv.CV_FOURCC(*list(sys.argv[i]))
    elif flag[0] == "-":
        if "s" in flag:
            show_video = True
        if "S" in flag:
            save_video = True
    i += 1


""" OPEN I/O INTERFACES """
# Open serial interface, if available
try:
    ser = serial.Serial(port, baudrate)
    ser.write("\n\nBEGIN TYR-VISION\n\n")
except:
    ser = None
    print "Couldn't open serial port!"

# Video dimensions
frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
print "Video resolution: %sx%s" % (frame_width, frame_height)

# Variables needed for saving the video
if save_video:
    folder = 'video_out/'  # eventually replace this with the SD card folder
    filename = time.strftime("%Y-%m-%d_%H:%M:%S.avi")
    path = folder + filename
    video_writer = cv2.VideoWriter(path, codec, 30, (frame_width, frame_height))


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
    threshold = 200
    white = cv2.inRange(frame, (threshold, threshold, threshold), (255, 255, 255))  # threshold detection of white regions
    contours, hierarchy = cv2.findContours(white, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)  # find contours in the thresholded image

    # Approximate outlines into polygons
    best_match = None # Variable to store best matching contour for U shape
    best_match_similarity = 1000 # Similarity of said contour to expected U shape. Defaults to an arbitrarily large number
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)  # smoothen the contours into simpler polygons
        # Filter through contours to detect a goal
        if cv2.contourArea(approx) > 1000 and len(approx) == 8:  # select contours with sufficient area and 8 vertices
            cv2.drawContours(frame, [approx], 0, (0,0,255), 2)  # draw the contour in red
            # test to see if this contour is the best match
            if check_match(approx):
                best_match = approx

    return best_match

def check_match(contour):
    """
    Checks if the contour is the U shape by first finding the point that's
    furthest to the bottom right. Since the points in a contour are always
    ordered counterclockwise, we know which point in the contour is supposed
    to match up to each point of the U shape based on its position in the
    contour relative to the bottom-left point. Based off of this, we check to
    make sure that the distance between two consecutive points is correctly
    greater-than or less-than the distance between the two preceding points.
    If the distances change in the same pattern as they should in the U shape,
    then we consider the contour to be a match of the U shape.
    """
    # Get lower right point by finding point furthest from origin (top left)
    start_index = get_start_index(contour)

    # Check if the match could be good
    # should_be_less is a list of whether or not each distance should be less
    # than the previous distance to be a U shape.
    should_be_less = [True, False, False, True, True, False, False]
    prev_dist = -1
    for i in range(0, 8):
        point_a = contour[(i + start_index) % 8][0]
        point_b = contour[(i + start_index + 1) % 8][0]
        dist = (point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2

        if i > 0 and (dist < prev_dist) != should_be_less[i-1]:
            return False

        prev_dist = dist

    return True

def get_start_index(contour):
    """
    Returns the index of the point that's furthest to the bottom and the left
    (furthest from the origin). This point is referred to as the start point
    and the indices of other points will be made relative to it.
    """
    biggest_dist = -1
    start_index = -1
    for i in range(0, len(contour)):
        # Technically the square of the distance, but it doesn't matter since
        # we are only comparing the distances relative to each other
        dist = contour[i][0][0]**2 + contour[i][0][1]**2
        if dist > biggest_dist:
            biggest_dist = dist
            start_index = i

    return start_index

def get_nth_point(contour, n, start_index=-1):
    """
    Returns the nth point in a contour relative to the start index. If no start
    index is provided, it is calculated using the get_start_index function.
    """
    if start_index == -1:
        start_index = get_start_index(contour)

    return contour[(start_index + n) % len(contour)][0]

def draw_goal(frame, target):
    """ Given the target controur, draws the extrapolated goal shape. """

    x,y,w,h = cv2.boundingRect(target)  # find a non-rotated bounding rectangle
    #cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)  # draw bounding rectangle in green

    # Draw goal contour based on the bounding box
    tape_x = int(w/10)
    tape_y = int(h/7)
    goal_x = x+tape_x
    goal_y = y-h+tape_y
    goal_w = int(w*4/5)
    goal_h = int(h*12/7)
    # circle parameters
    radius = int(goal_w/2)
    center = (goal_x+radius, goal_y+radius)
    cv2.rectangle(frame, (goal_x, goal_y+radius), (goal_x+goal_w, goal_y+goal_h), (255, 0, 255), -1)  # draw the goal bounding box in purple
    cv2.circle(frame, center, radius, (255, 0, 255), -1)


def target_center(target):
    """ Returns the top center point of a given target contour """
    left_pt = get_nth_point(target, 6)
    right_pt = get_nth_point(target, 1)
    return int((left_pt[0] + right_pt[0]) / 2), int((left_pt[1] + right_pt[1]) / 2)

def image_center():
    """ Returns the center coordinate of the image """
    return int(frame_width/2), int(frame_height/2)


def draw_base_HUD(frame):
    """ Draw base crosshairs in black on the given frame. Returns the frame's
    center coordinate. """
    center_x, center_y = image_center()

    cv2.line(frame, (center_x, 0), (center_x, frame_height), (0, 0, 0), 2) # Vertical line
    cv2.line(frame, (0, center_y), (frame_width, center_y), (0, 0, 0), 2) # Horizontal line
    cv2.circle(frame, (center_x, center_y), 25, (0, 0, 0), 2) # center circle
    return center_x, center_y


def draw_targeting_HUD(frame, target):
    """ Draws the target, goal (via the draw_goal() function),
    displacement vector, and a text box showing the target's displacement. """

    cv2.rectangle(frame, (0, 0), (320, 48), (0, 0, 0), -1) # Rectangle where text will be displayed
    if target is None:
        cv2.putText(frame, "No target found", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        #pause = True
    else:  # draw the best match and its bounding box
        cv2.drawContours(frame, [target], 0, (255, 255, 0), 3) # Draw target in cyan
        draw_goal(frame, target)

        center_x, center_y = image_center()
        target_x, target_y = target_center(target)

        # Show the displacement as a vector in Cartesian coordinates (green)
        displacement_x = target_x - center_x # Positive when to the right of center
        displacement_y = center_y - target_y # Positive when above center
        cv2.line(frame, (center_x, center_y), (target_x, target_y), (0, 255, 0), 5)
        # Overlay the displacement values as text
        text = "<%d, %d>" % (displacement_x, displacement_y)
        cv2.putText(frame, "%s" % text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        # Send displacement data over serial
        send_data(displacement_x, displacement_y)


def draw_fps(frame, fps):
    """ Draws the given framerate onto the given frame """
    cv2.rectangle(frame, (0, 48), (320, 96), (0, 0, 0), -1)
    cv2.putText(frame, "FPS: %f" % fps, (16, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))


def send_data(*data):
    """
    Takes a list of data to send and sends it over serial in a comma
    separated list. Each data element in a packet is separated by a tab, and each
    packet is separated by a linefeed.

    Example: If the displacement vector is <-210, 42> then we send:
    -210\t42\n

    """
    if ser != None:
        string = ""
        for i in range(0, len(data)):
            string += str(data[i]) + "\t"
        string = string[:-2] # Remove trailing ', '
        string += '\n'  # linefeed at end of line
        #print string,  # print without an extra linefeed
        ser.write(string)


""" VIDEO PROCESSING LOOP """
prev_time = time.time()
cur_time = time.time()

while(cap.isOpened()):
    pause = False
    ret, frame = cap.read()  # read a frame
    prev_time = cur_time
    cur_time = time.time()
    if ret:
        best_match = find_best_match(frame)  # perform detection before drawing the HUD
        draw_targeting_HUD(frame, best_match)
        draw_base_HUD(frame)
        draw_fps(frame, 1.0 / (cur_time - prev_time))

        if show_video:
            cv2.imshow('tyr-vision', frame)  # show the image output on-screen

        if save_video:
            video_writer.write(frame)

        k = cv2.waitKey(1)  # wait 1ms for a keystroke
        if k == ord('q') or k == 27:  # exit with the 'q' or 'esc' key
            print "Exiting playback!"
            break
        elif k == ord(' '):  # pause with the spacebar
            pause = True

        if pause:
            print "Pausing video"
            while True:
                if cv2.waitKey(1) == ord(' '):  # resume with the spacebar
                    print "Resuming video"
                    break
    else: # Close program when video ends
        break


""" CLEAN UP """
cap.release()  # close the video interface
cv2.destroyAllWindows()  #LinuxWorldDomination
if ser != None:
    ser.close()  # close the serial interface
