# videooutput.py
#
# Module for writing video output to the disk.

""" LIBRARY IMPORTS """
import time
import cv2

# LOCAL MODULE IMPORTS
import settings
import videoinput


video_writer = None
filetype = 'avi'


def start_recording(codec, filename=time.strftime("%Y-%m-%d_%H-%M-%S")):
    """ Start recording video to the disk """
    global video_writer
    folder = 'video_out/'  # eventually replace this with the SD card folder
    # TODO: also include branch name and/or commit ID
    path = folder + filename + '.' + filetype
    print "Saving video to: %s" % path

    height = videoinput.frame_height
    if settings.sidebyside:
        width = 2*videoinput.frame_width
    else:
        width = videoinput.frame_width

    try:
        video_writer = cv2.VideoWriter(path, codec, 30, (width, height))
    except:
        print "Failed to open video file for writing!"


def write(frame):
    """ Write the given frame to the output file. """
    video_writer.write(frame)



def stop_recording():
    """ Stop recording video to the disk """
    global video_writer
    video_writer = None
    print "Stopped recording"
