# networking.py
#
# Module for networking to the Driver Station
#
# IP camera code from: https://gist.github.com/thearn/5562029
import base64
import socket
import videooutput
import cv2
import urllib2
import numpy as np

streaming = False
frame_until_stream = 2

s = None
start_stop_video_socket = None
IP = "10.0.8.202"
PORT_STREAMING = 56541
PORT_START_STOP = 56543


class ipCamera(object):

    def __init__(self, url, user=None, password=None):
        self.url = url
        auth_encoded = base64.encodestring('%s:%s' % ("root", "password"))[:-1]
        self.req = urllib2.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def get_frame(self):
        response = urllib2.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR


def try_connection_streaming():
    """ Try to create the socket connection. """
    global streaming
    global s

    while 1:
        if not streaming:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IP, PORT_STREAMING))
            s.listen(1)
            print "Listening"
            s = s.accept()[0]

            streaming = True
#            except:
#            streaming = False


# TODO: make this function take IP and PORT as arguments
def try_connection_start_stop_writing():
    """ Try to create the socket connection. """
    global start_stop_video_socket

    start_stop_video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_stop_video_socket.bind((IP, PORT_START_STOP))
    start_stop_video_socket.listen(1)
    print "Listening"
    start_stop_video_socket = start_stop_video_socket.accept()[0]

    video_writer_listen()


def video_writer_listen():
    try:
        while 1:
            name = start_stop_video_socket.recv(1024)
            if name != chr(0):
                videooutput.start_recording("avi", filename=name)
            else:
                videooutput.start_recording("avi", filename=name)
            start_stop_video_socket.recv(1024)
            videooutput.stop_recording()
    except KeyboardInterrupt:
        pass



def send_video(frame):
    try:
        data = ""  # the data we are going to send
        counter = 120  # size of each packet
        sent = 0  # for debugging
        s.send(chr(0))  # Send a null byte to mark a new frame
        for i in xrange(120):  # height
            for j in xrange(160):  # width
                if counter == 1:  # if we need to send

                    s.send(chr(sent) + data + chr(frame[i, j]))  # send the data
                    data = ""
                    counter = 120
                    sent += 1
                else:
                    data += chr(frame[i][j])
                    counter -= 1
        # lost = s.recv(1024)

        # for i in xrange(len(lost)):
        #     num_lost = ord(lost[i])
        #     s.send(chr(num_lost)+all_parts[num_lost])
    except:
        print "Error In Send Video"
        pass
