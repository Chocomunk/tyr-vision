# videoinput.py
#
# Module for getting video input from either a webcam or a video file.

import cv2
import networking

#cap = cv2.VideoCapture('video_in/12ft.mp4')
cap = None
frame_width = 0
frame_height = 0
frame_area = 0

using_axis = True


def open_stream(device):
    """
    Opens the video input device. By default, the file video_input/12ft.mp4 is
    opened. If an integer X is specified, it opens the camera device at
    /dev/videoX and sets its resolution to 1920x1080. Otherwise, a video file of
    the specified name within video_input is opened.
    """

    global cap
    global frame_width
    global frame_height
    global frame_area

    if device is None:
        device = '12ft.mp4'

    try:

        # an integer X indicates the webcam address, ie. /dev/videoX
        cap = cv2.VideoCapture(int(device))
        # set resolution manually
        # the Logitech C920 is 1080p
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
        print "Opened webcam at: /dev/video%s" % device
    except:
        
       # if it's not an integer, it's a filepath for a video
        cap = cv2.VideoCapture("video_in/" + device)
        print "Opened video file at: %s" % device
    # Figure out the video dimensions
    frame_width = 400#int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    frame_height = 640 #int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    if frame_width == frame_height == 0:
        print "ERROR: resolution is 0x0; falling back to 12ft.mp4"
        cap = cv2.VideoCapture('video_in/12ft.mp4')
        frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    frame_area = frame_width * frame_height
    print "Video resolution: %sx%s" % (frame_width, frame_height)


def close_stream():
    cap.release()
