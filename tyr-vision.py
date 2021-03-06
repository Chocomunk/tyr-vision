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
# import serialoutput
import networking
from networktables import NetworkTable
import urllib2

IP = "roborio-8-frc.local"

NetworkTable.setIPAddress(IP)
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("AutoAlign")



avg_distance = None

GOAL_INCHES = 18

# a = 122520
# b = -3203.4
# c = 23.766

x = -620090
y = -98.894
c = 620650
d = 603600
g = -719350
h = -0.22849

""" PROCESS COMMAND LINE FLAGS """
settings.process_arguments(sys.argv)
settings.print_settings()

""" INITIALIZE MODULES """
# serialoutput.init_serial(settings.port, settings.baudrate)
videoinput.open_stream(settings.device)

if settings.save_video:
    t0 = Thread(target=videooutput.start_recording, args=(settings.codec,))
    t0.daemon = True
    t0.start()
    # videooutput.start_recording(settings.codec)


t1 = Thread(target=networking.try_connection_streaming)
t2 = Thread(target=networking.try_connection_start_stop_writing)

t1.daemon = True  # thread automatically closes when main thread closes
t1.start()

t2.daemon = True
t2.start()


""" VIDEO PROCESSING LOOP """
initial_time = time.time() # Time the program was started
total_frames = 0 # Number of frames analyzed
times = [time.time()] # List of the times of the last 10 analyzed frames

stream = urllib2.urlopen("http://10.0.8.200/mjpg/video.mjpg")
bytes=''
###
# If using axis: 
while True:

    bytes += stream.read(1024)
    # 0xff 0xd8 is the starting of the jpeg frame
    a = bytes.find('\xff\xd8')
    # 0xff 0xd9 is the end of the jpeg frame
    b = bytes.find('\xff\xd9')
    # Taking the jpeg image as byte stream
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        # Decoding the byte stream to cv2 readable matrix format
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),1)
###
# If using Webcam
# while videoinput.cap.isOpened():
###
    # frame = networking.read_from_axis()

        pause = False
        total_frames += 1
        times.append(time.time())
        if len(times) > 10: times.pop(0)

        # frame = videoinput.cap.get_frame()
        ret = True
        # ret, frame = videoinput.cap.read()  # read a frame
        if settings.sidebyside:
            original_frame = frame.copy()

        if ret:
            best_match = targeting.find_best_match(frame)  # perform detection before drawing the HUD
            # frame = networking.read_from_axis()

            if best_match is not None:
                scaler = cv2.contourArea(best_match) / 256000#videoinput.frame_area 

                if avg_distance is not None:
                    avg_distance = (scaler+avg_distance)/2
                else:
                    avg_distance = scaler 
                print "Contounr area / video area: " + str(scaler)

                distance = (x * (np.e**scaler)) - (y * np.log(scaler)) + c + (d*scaler) - (g*(scaler**2)) - (h/scaler)
                distance = distance * 12
                distance += 10 # numpy.log((a*(scaler**2)+b*scaler+c)*12
                displacement_x, displacement_y, width, height = videooverlay.draw_targeting_HUD(frame, best_match)

                pixels_to_inches = GOAL_INCHES / (targeting.get_nth_point(best_match, 1)[0] - targeting.get_nth_point(best_match, 6)[0]) 

                x_inches_displacement = pixels_to_inches*displacement_x

                x_angle_displacement = np.arctan(x_inches_displacement/distance)*57.2958 # Radians to inches

                table.putNumber("SkewAngle", x_angle_displacement)
                table.putNumber("Distance", distance)
                table.putNumber("xDisplacement", displacement_x)

                print "Distance to the goal" + str(distance)
                print "Inches offset" + str(x_inches_displacement)
                print "Angle Offset:" + str(x_angle_displacement)




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
            # videooverlay.draw_fps(frame, fps)

            if settings.sidebyside:  # render original & processed images side by side
                frame = np.hstack((original_frame, frame))

            if settings.show_video:
                cv2.namedWindow("tyr-vision", cv2.WINDOW_NORMAL)  # allow resizing

                try:
                    import pyautogui
                    screen_width, screen_height = pyautogui.size()
                    cv2.resizeWindow("tyr-vision", settings.VIDEO_WIDTH, settings.VIDEO_HEIGHT)
                except: pass
                        # cv2.resizeWindow("tyr-vision", 640, 400)
                    # print "Couldn't import pyautogui"

                cv2.imshow('tyr-vision', cv2.resize(frame, (settings.DISPLAY_HEIGHT, settings.DISPLAY_WIDTH)))  # show the image output on-screen

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

print "AVG" + str(avg_distance)
