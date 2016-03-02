# networking.py
#
# Module for networking to the Driver Station

import socket


streaming = False
frame_until_stream = 2

s = None
IP = "10.0.8.202"
PORT = 56541


# TODO: make this function take IP and PORT as arguments
def try_connection():
    """ Try to create the socket connection. """
    global streaming
    global s

    while 1:
        if not streaming:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IP, PORT))
            s.listen(1)
            print "Listening"
            s = s.accept()[0]

            streaming = True
#            except:
#            streaming = False


def send_video(frame):
    try:
        data = ""  # the data we are going to send
        counter = 120  # size of each packet
        sent = 0  # for debugging
        s.send(chr(0))  # Send a null byte to mark a new frame
        for i in xrange(120):  #height
            for j in xrange(160): #width
                if counter == 1: # if we need to send

                    s.send(chr(sent)+data+chr(frame[i,j]))#send the data
                    data = ""
                    counter = 120
		    sent += 1
                else:
                    data+=chr(frame[i][j])
                    counter-=1
        # lost = s.recv(1024)

        # for i in xrange(len(lost)):
        #     num_lost = ord(lost[i])
        #     s.send(chr(num_lost)+all_parts[num_lost])
    except:
        print "Error In Send Video"
        pass

