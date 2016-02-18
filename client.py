import socket
import cv2
import numpy

SERVER_IP = "10.0.8.202"
SERVER_PORT = 56541												   
save_video = False

HEIGHT = 120
WIDTH = 160
BUFFER_SIZE = 120

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((SERVER_IP,SERVER_PORT))

def decode_data(data):
	pixels=list(data)
	if len(data) != HEIGHT*WIDTH: return None
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
		print "In loop"
		#while s.recv(1) != chr(0): pass # null byte marks a new frame
		
		data = ""

		for i in xrange(160):

			incoming_packet = s.recv(120)
			print len(incoming_packet)
			if incoming_packet != chr(0): data += incoming_packet
			else: 
				data = None
				break
		if data != None:
			frame = decode_data(data)
			print frame
			#frame = decode_data(''.join([s.recv(BUFFER_SIZE) for i in xrange(128)]))
			#import ipdb; ipdb.set_trace()
			if frame != None:
				cv2.imshow('tyr-vision', cv2.resize(frame,(1280,720)))  # show the image output on-screen
				cv2.waitKey(50)
				if save_video:
					pass
#except KeyboardInterrupt:
#	pass
main()
