import socket
import cv2
import numpy
from threading import Thread


SERVER_IP = "10.0.8.202"
SERVER_PORT = 56541
DATA_PORT = 56541
VIDEO_START_STOP_PORT = 56543

save_video = False

HEIGHT = 120
WIDTH = 160
BUFFER_SIZE = 120

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
except:
    print "Video Streaming Socket Could not be made"


try:
    data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data.connect((SERVER_IP, DATA_PORT))
except:
    print "data socket could not be make"

try:
    record_socket = socket.socket.(socket.AF_INET, socket.SOCK_STREAM))
    record_socket.connect((SERVER_IP, VIDEO_START_STOP_PORT))


def startStopVideo():
    print "If you would like to start recording Video, enter the name of the Video Here. OtherWise, do nothing"
    vid_name = raw_input("File Name: ")
    record_socket.send(chr(0))
    raw_input("To stop recording Video, hit enter")
    record_socket.send(chr(1))
    startStopVideo()

Thread(target = startStopVideo).start()
last_frame = chr(0) * HEIGHT * WIDTH

HUD_TEXT = ""


def decode_data(data):
    pixels = list(data)

    if len(data) != HEIGHT * WIDTH:
        return None
    pixel_index = 0
    frame = numpy.ndarray(shape=(HEIGHT, WIDTH), dtype=numpy.uint8)

    for i in xrange(HEIGHT):
        for j in xrange(WIDTH):
                frame[i][j] = numpy.uint8(ord(pixels[pixel_index]))
                pixel_index += 1
    return frame


def update_hud_text():
    while 1:
        global HUD_TEXT
        HUD_TEXT = data.recv(1024)


def main():
    Thread(target=update_hud_text).start()
    # try:
    while 1:
        while s.recv(1) != chr(0):
            pass  # null byte marks a new frame

        data = {}
        i = 0
        for i in xrange(160):

            packet = s.recv(121)
            print len(packet)
            frame_number = ord(packet[0])
            incoming_packet = packet[1:]
            if len(incoming_packet) != 120:
                incoming_packet += last_frame[i * 120 + len(incoming_packet):(i + 1) * 120]
            # incoming_packet+=last_frame[((i*120)+len(incoming_packet)):((i*120)+(120))]
            if packet != chr(0):
                data[frame_number] = incoming_packet
            else:
                data = None
                break
        if data is not None:
            packets = ""
            for i in xrange(160):
                try:
                    packets += data[i]
                except:
                    packets += chr(0) * 120
            frame = decode_data(packets)
            # frame = decode_data(''.join([s.recv(BUFFER_SIZE) for i in xrange(128)]))
            # import ipdb; ipdb.set_trace()
            if frame is not None:
                y0, dy = 50, 4
                for i, line in enumerate(HUD_TEXT.split("\n")):
                    y = y0 + i * dy
                    cv2.putText(frame, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                cv2.imshow('tyr-vision', cv2.resize(frame, (1280, 720)))  # show the image output on-screen
                cv2.waitKey(50)
                if save_video:
                    pass
# except KeyboardInterrupt:
#    pass
main()
