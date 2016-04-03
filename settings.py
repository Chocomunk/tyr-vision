# settings.py
#
# Module for all the default settings
#

import cv2
import re
""" Serial Output """
#port = '/dev/ttyS0' # primary DB9 RS-232 port
#port = '/dev/ttyUSB0' # primary USB-serial port
port = '/dev/ttyTHS0'  # primary 1.8V UART on the Jetson
baudrate = 9600
#baudrate = 15200

""" Video Settings """
device = None
print_fps = False
show_video = False
save_video = False
sidebyside = False
codec = None # cv2.cv.CV_FOURCC('M', 'J', 'P', 'G')

DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 480

def process_arguments(args):
    """
    Processes the given list of arguments to override the default settings.

    There are many nested conditionals here; be careful to not mess up the
    indentations.
    """
    global port
    global baudrate
    global device
    global print_fps
    global show_video
    global save_video
    global sidebyside
    global codec

    i = 1
    while i < len(args):
        flag = args[i]
        print flag
	if flag[:2] == "--":
            if flag == "--show":
                show_video = True
            elif flag == "--save":
                save_video = True
            elif flag == "--sidebyside":
                sidebyside = True
            elif flag == "--fps":
                print_fps = True
            elif flag == "--device":
                i += 1
                device = args[i]
            elif flag == "--port":
                i += 1
                port = args[i]
            elif flag == "--baudrate":
                i += 1
                baudrate = args[i]
            elif flag == "--codec":
                i += 1
                codec = cv2.cv.CV_FOURCC(*list(args[i]))
            elif flag[:5] == "--vr:":
		global DISPLAY_HEIGHT
		global DISPLAY_WIDTH
		DISPLAY_WIDTH = int(flag[5:flag.rindex("x")])
		DISPLAY_HEIGHT = int(flag[flag.rindex("x")+1:])
        elif flag[0] == "-":
            if "s" in flag:
                show_video = True

            if "S" in flag:
                save_video = True

        i += 1


def print_settings():
    """ Print the current settings.  """
    print "\nSETTINGS"
    print "Serial port:\t%s @ %s baud" % (port, baudrate)
    print "Capture device:\t%s" % device
    print "Show video?\t%s" % show_video
    print "Save video?\t%s" % save_video
    print "Output codec:\t%s" % codec
    print # extra linefeed


# TODO: write unittests
