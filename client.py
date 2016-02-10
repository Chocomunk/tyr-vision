import socket
import cv2
import numpy

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5005												   
save_video = False

HEIGHT = 180
WIDTH = 320
BUFFER_SIZE = 400

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((SERVER_IP,SERVER_PORT))

def decode_data(data):
	pixels=list(data)
	pixel_index = 0
	frame = numpy.ndarray(shape=(HEIGHT,WIDTH),dtype=numpy.uint8)

	for i in xrange(HEIGHT):
		for j in xrange(WIDTH):
				frame[i][j] = numpy.uint8(ord(pixels[pixel_index]))
				pixel_index+=1
	return frame


def main():

#try:
	while 1:
		print "Stared Decode"
		frame = cv2.cvtColor(decode_data(''.join([s.recv(BUFFER_SIZE) for i in xrange(144)])), cv2.COLOR_GRAY2RGB)
		print "Finished Decode"
		#import ipdb; ipdb.set_trace()
		cv2.imshow('tyr-vision', cv2.resize(frame,(1280,720)))  # show the image output on-screen
		cv2.waitKey(50)
		if save_video:
			pass
#except KeyboardInterrupt:
#	pass
main()
