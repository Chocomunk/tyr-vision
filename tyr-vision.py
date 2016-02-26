#!/usr/bin/env python2
#
# tyr-vision.py
#
# Team 8 Stronghold vision program
#


""" LIBRARY IMPORTS """
from __future__ import division  # always use floating point division
import sys
import time
import cv2

""" LOCAL MODULE IMPORTS """
import videoinput
import videooutput
import targeting
import videooverlay
import serialoutput
import networking


""" DEFAULT SETTINGS """
""" Serial Output """
#port = '/dev/ttyS0' # primary DB9 RS-232 port
#port = '/dev/ttyUSB0' # primary USB-serial port
port = '/dev/ttyTHS0'  # primary 1.8V UART on the Jetson
baudrate = 9600
#baudrate = 15200

""" Video Settings """
device = None
show_video = False
save_video = False
codec = cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')



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
            device = sys.argv[i]
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


""" INITIALIZE MODULES """
serialoutput.init_serial(port, baudrate)
videoinput.open_stream(device)

if save_video:
    videooutput.start_recording(codec)


""" VIDEO PROCESSING LOOP """
prev_time = time.time()
cur_time = time.time()

while(videoinput.cap.isOpened()):
    pause = False
    ret, frame = videoinput.cap.read()  # read a frame
    prev_time = cur_time
    cur_time = time.time()
    if ret:
        best_match = targeting.find_best_match(frame)  # perform detection before drawing the HUD
        videooverlay.draw_targeting_HUD(frame, best_match)
        # TODO: serial output should be called in this loop, NOT draw_targeting_HUD!
        videooverlay.draw_base_HUD(frame)
        fps = int(1.0 / (cur_time - prev_time))
        #print "FPS: %s" % fps
        videooverlay.draw_fps(frame, fps)

        if show_video:
            cv2.imshow('tyr-vision', frame)  # show the image output on-screen

        try:
            videooutput.video_writer.write(frame)
        except:
            pass

        k = cv2.waitKey(1)  # wait 1ms for a keystroke
        if k == ord('q') or k == 27:  # exit with the 'q' or 'esc' key
            print "Exiting playback!"
            break
        elif k == ord(' '):  # pause with the spacebar
            pause = True

        if pause:
            print "Pausing video"
            videooutput.stop_recording()
            while True:
                if cv2.waitKey(1) == ord(' '):  # resume with the spacebar
                    print "Resuming video"
                    break
    else: # Close program when video ends
        break


""" CLEAN UP """
videoinput.cap.release()  # close the video interface
cv2.destroyAllWindows()  #LinuxWorldDomination
if serialoutput.ser != None:
    serialoutput.ser.close()  # close the serial interface
