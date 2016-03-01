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
import socket
from threading import Thread

""" LOCAL MODULE IMPORTS """
import settings
import videoinput
import videooutput
import targeting
import videooverlay
import serialoutput
import networking


""" PROCESS COMMAND LINE FLAGS """
settings.process_arguments(sys.argv)
settings.print_settings()

""" INITIALIZE MODULES """
serialoutput.init_serial(settings.port, settings.baudrate)
videoinput.open_stream(settings.device)

if settings.save_video:
    videooutput.start_recording(settings.codec)


"""
Video Streaming
"""
streaming = False
frame_until_stream = 2

s = None
IP = "10.0.8.202"
PORT = 56541


def try_connection():
    """Try to create the socket connection."""
    global streaming
    global s

    while 1:
        if not streaming:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IP, PORT))
            s.listen(1)
            print "Listening"
            s = s.accept()[0]

            streaming = True
#            except:
#            streaming = False


Thread(target=try_connection).start()


def send_video(frame):
    try:
        data = ""  # the data we are going to send
        counter = 120  # size of each packet
        sent = 0  # for debugging
        s.send(chr(0))  # Send a null byte to mark a new frame
        for i in xrange(120):  #height
            for j in xrange(160): #width
                if counter == 1: # if we need to send

                    sent+=1 # for debugging
                    s.send(chr(sent)+data+chr(frame[i,j]))#send the data
                    data = ""
                    counter = 120

                else:
                    data+=chr(frame[i][j])
                    counter-=1
        # lost = s.recv(1024)

        # for i in xrange(len(lost)):
        #     num_lost = ord(lost[i])
        #     s.send(chr(num_lost)+all_parts[num_lost])
    except:
        print "Error In Send Video"
        pass



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

        try:
            if streaming and frame_until_stream == 0:
                send_video(cv2.cvtColor(cv2.resize(frame,(160,120)), cv2.COLOR_BGR2GRAY))
                frame_until_stream = 2
            else: frame_until_stream -=1
        except:
            print "Error in video streaming Loop"
            pass

        fps = int(1.0 / (cur_time - prev_time))
        #print "FPS: %s" % fps
        videooverlay.draw_fps(frame, fps)

        if settings.show_video:
            cv2.imshow('tyr-vision', frame)  # show the image output on-screen

        try:
            videooutput.write(frame)
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
            while True:
                if cv2.waitKey(1) == ord(' '):  # resume with the spacebar
                    print "Resuming video"
                    break
    else:  # Close program when video ends
        break


""" CLEAN UP """
videoinput.close_stream()  # close the video interface
cv2.destroyAllWindows()  #LinuxWorldDomination
serialoutput.close()
