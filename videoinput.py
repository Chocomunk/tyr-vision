# videoinput.py
#
# Module for getting video input from either a webcam or a video file.

import cv2

#cap = cv2.VideoCapture('video_in/12ft.mp4')
cap = None
frame_width = 0
frame_height = 0


def open_stream(device):
    global cap
    global frame_width
    global frame_height

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

    # Video dimensions
    frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    if frame_width == frame_height == 0:
        print "ERROR: resolution is 0x0; falling back to 12ft.mp4"
        cap = cv2.VideoCapture('video_in/12ft.mp4')
        frame_width = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    print "Video resolution: %sx%s" % (frame_width, frame_height)

