# videooutput.py
#
# Module for writing video output to the disk.

import cv2

def start_recording(codec, filename = time.strftime("%Y-%m-%d_%H-%M-%S")):
    """ Start recording video to the disk """
    global video_writer
    folder = 'video_out/'  # eventually replace this with the SD card folder
    filetype = 'avi'
    # TODO: also include branch name and/or commit ID
    path = folder + filename + '.' + filetype
    print "Saving video to: %s" % path
    video_writer = cv2.VideoWriter(path, codec, 30, (videoinput.frame_width, videoinput.frame_height))

def stop_recording():
    """ Stop recording video to the disk """
    global video_writer
    video_writer = None
    print "Stopped recording"
