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
from threading import Thread
import cv2
import numpy as np

# LOCAL MODULE IMPORTS

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
    # videooutput.start_recording(settings.codec)


t1 = Thread(target=networking.try_connection_streaming).start()
t2 = Thread(target=networking.try_connection_start_stop_writing).start()

t1.daemon = True  # thread automatically closes when main thread closes
t1.start()

t2.daemon = True
t2.start()


""" VIDEO PROCESSING LOOP """
initial_time = time.time() # Time the program was started
total_frames = 0 # Number of frames analyzed
times = [time.time()] # List of the times of the last 10 analyzed frames

while(videoinput.cap.isOpened()):
    pause = False
    total_frames += 1
    times.append(time.time())
    if len(times) > 10: times.pop(0)

    ret, frame = videoinput.cap.read()  # read a frame
    if settings.sidebyside:
        original_frame = frame.copy()

    if ret:
        best_match = targeting.find_best_match(frame)  # perform detection before drawing the HUD
        videooverlay.draw_targeting_HUD(frame, best_match)
        # TODO: serial output should be called in this loop, NOT draw_targeting_HUD!
        videooverlay.draw_base_HUD(frame)

        try:
            # TODO: these variables should be moved to settings.py
            if networking.streaming and networking.frame_until_stream < 1:
                networking.send_video(cv2.cvtColor(cv2.resize(frame, (160, 120)), cv2.COLOR_BGR2GRAY))
                networking.frame_until_stream = 2
            else: networking.frame_until_stream -=1
        except:
            print "Error in video streaming Loop"
            pass

        fps = int(1.0 / (times[-1] - times[-2]))
        ten_fps = int(min(10.0, total_frames) / (times[-1] - times[0]))
        avg_fps = int(total_frames / (times[-1] - initial_time))
        if settings.print_fps: print "%s\t%s\t%s" % (fps, ten_fps, avg_fps)
        videooverlay.draw_fps(frame, fps)

        if settings.sidebyside:  # render original & processed images side by side
            frame = np.hstack((original_frame, frame))

        if settings.show_video:
            cv2.namedWindow("tyr-vision", cv2.cv.CV_WINDOW_NORMAL)  # allow resizing

            try:
                import pyautogui
                screen_width, screen_height = pyautogui.size()
                cv2.resizeWindow("tyr-vision", screen_width, screen_height)
            except:
                print "Couldn't import pyautogui"

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
