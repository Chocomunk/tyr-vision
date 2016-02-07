import socket
import cv2
import numpy

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5005

HEIGHT = 720
WIDTH = 1280
BUFFER_SIZE = 1350

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto('',(SERVER_IP,SERVER_PORT))

save_video = False


def decode_data(data):
	pixels=list(data)
	pixel_index = 0
	frame = numpy.ndarray(shape=(HEIGHT,WIDTH,3))

	for i in xrange(HEIGHT):
		for j in xrange(WIDTH):
			for k in xrange(3):

				frame[i][j][k] = numpy.float64(ord(pixels[pixel_index]))
				pixel_index+=1
				
	return frame

			



try:
	while 1:
		frame = decode_data(''.join([s.recv(BUFFER_SIZE) for i in xrange(2048)]))
		print "GOT FRAME!"
		import ipdb; ipdb.set_trace()
		cv2.imshow('tyr-vision', frame)  # show the image output on-screen
		if save_video:
			pass
except KeyboardInterrupt:
	pass
