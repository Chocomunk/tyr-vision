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
    t0 = Thread(target=videooutput.start_recording, args=(settings.codec,))
    t0.daemon = True
    t0.start()
    #videooutput.start_recording(settings.codec)

t1 = Thread(target=networking.try_connection)  # networking thread
t1.daemon = True  # thread automatically closes when main thread closes
t1.start()



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
            # TODO: these variables should be moved to settings.py
            if networking.streaming and networking.frame_until_stream < 1:
                networking.send_video(cv2.cvtColor(cv2.resize(frame,(160,120)), cv2.COLOR_BGR2GRAY))
                networking.frame_until_stream = 2
            else: networking.frame_until_stream -=1
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
