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
import serial


""" Video Streaming """


import socket 
from threading import Thread


IP = "192.168.0.101"
PORT = 5005


s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((IP,PORT))
s.listen(1)
s=s.accept()[0]

frame_until_stream = 2

#except:
#	print "Sockets aren't working"
#	s=None
streaming = True

#if streaming:
#	user=s.recvfrom(0)[1]
#	print user


""" Serial Output """
#port = '/dev/ttyS0' # primary DB9 RS-232 port
#port = '/dev/ttyUSB0' # primary USB-serial port
port = '/dev/ttyTHS0'  # primary 1.8V UART on the Jetson

baudrate = 9600
#baudrate = 15200

try:
    ser = serial.Serial(port, baudrate)
    ser.write("\n\nBEGIN TYR-VISION\n\n")
except:
    ser = None
    print "Couldn't open serial port!"


""" Video Input Settings """
cap = cv2.VideoCapture(0)  # stream from webcam
#cap = cv2.VideoCapture('close-up-mini-U.mp4')  # https://goo.gl/photos/ECz2rhyqocxpJYQx9
#cap = cv2.VideoCapture('12Feet.mp4')  # https://goo.gl/photos/ZD4pditqMNt9r3Vr6

# Video options
show_video = False
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
    x, y, w, h = cv2.boundingRect(target)
    return int(x + w/2), y


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
    """ Draws the target, goal (via the draw_goal() function), crosshair lines,
    displacment line, and a text box showing the target's displacement. """

    cv2.rectangle(frame, (0, 0), (320, 48), (0, 0, 0), -1) # Rectangle where text will be displayed
    if target is None:
        cv2.putText(frame, "No target found", (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        #pause = True
    else:  # draw the best match and its bounding box
        cv2.drawContours(frame, [target], 0, (255, 255, 255), 3) # Draw target in cyan

        draw_goal(frame, target)
        center_x, center_y = image_center()

        # Display target crosshairs
        target_x, target_y = target_center(target)
        """
        cv2.line(frame, (0, target_y), (frame_width, target_y), (255, 128, 0), 2) # Horizontal line through target center in dark blue
        cv2.line(frame, (target_x, 0), (target_x, frame_height), (255, 128, 0), 2) # Vertical line through target center in dark blue
        cv2.circle(frame, (target_x, target_y), 25, (255, 128, 0), 2)
        """

        # Show the displacement as a vector in Cartesian coordinates (green)
        displacement_x = target_x - center_x
        displacement_y = center_y - target_y
        cv2.line(frame, (center_x, center_y), (target_x, target_y), (0, 255, 0), 5)
        text = "<%d, %d>\n" % (displacement_x, displacement_y)
        cv2.putText(frame, "%s" % text, (16, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        if ser != None:
            # send displacement data over serial
            ser.write(text)

def send_video(frame):
	data = "" # the data we are going to send
	counter = 150 # size of each packet
	sent = 0 # for debugging
	s.send(chr(0)) # Send a null byte to mark a new frame
	for i in xrange(120): #height
		for j in xrange(160): #width
			if counter == 1: # if we need to send
				sent+=1 # for debugging
				s.send(data+chr(frame[i,j]))#send the data 
				data = ""
				counter = 150
						
			else:
				data+=chr(frame[i][j])
				counter-=1
	print sent


""" BEGIN video processing loop """
while(cap.isOpened()):
    pause = False
    ret, frame = cap.read()  # read a frame
    if ret:
	if streaming and frame_until_stream == 0:
                send_video(cv2.cvtColor(cv2.resize(frame,(160,120)), cv2.COLOR_BGR2GRAY))
                frame_until_stream = 2
        else: frame_until_stream -=1
	

        best_match = find_best_match(frame)  # perform detection before drawing the HUD
        draw_base_HUD(frame)
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
ser.close()  # close the serial interface
