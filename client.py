import socket
import cv2

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5005

BUFFER_SIZE = 1024

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto('',SERVER_IP,SERVER_PORT)

save_video = False

try:
	while 1:
		frame = s.recv(1024)
		cv2.imshow('tyr-vision', frame)  # show the image output on-screen
		if save_video:
			pass
except KeyboardInterrupt:
	pass