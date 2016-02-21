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


last_frame = chr(0) * WIDTH*HEIGHT
def decode_data(data):
	pixels=list(data)

	if len(data) != HEIGHT*WIDTH: return None
	last_frame = pixels
	pixel_index = 0
	frame = numpy.ndarray(shape=(HEIGHT,WIDTH),dtype=numpy.uint8)
		
	for i in xrange(HEIGHT):
		for j in xrange(WIDTH):
				frame[i][j] = numpy.uint8(ord(pixels[pixel_index]))
				pixel_index+=1
	last_frame = frame
	return frame


def main():

#try:
	while 1:
		print "In loop"
		#while s.recv(1) != chr(0): pass # null byte marks a new frame
		
		data = {}
        not_recived = []
		for i in xrange(160):

			packet = s.recv(121)
			frame_number = ord(packet[0])
			incoming_packet = packet[1:]
			if len(incoming_packet) != 120: 
				not_recived.append(frame_number)
                #incoming_packet+=last_frame[((i*120)+len(incoming_packet)):((i*120)+(120))]
			print len(incoming_packet)
			if incoming_packet != chr(0): data[frame_number] = incoming_packet
			else: 
				data = None
				break
        for i in xrange(160):
            if i not in data: not_recived.append(i)

        for i in not_recived:
            s.send(''.join([chr(i) for i in not_recived]))
        for i in not_recived:
            packet = s.recv(121)
            pix = packet[1:]
            if len(pix) != 120:
                data[ord(packet[0])] = pix + chr(0) * (120-len(pix))
            else: data[ord(packet[0])] = pix

		if data != None:
			packets = ""
			for i in xrange(160):
				try:
					packets+=data[i]
				except:
					packets+=last_frame[i*120:(i+1)*120]
					
			frame = decode_data(packets)
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
