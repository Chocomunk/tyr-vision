# serialoutput.py
#
# Module for serial output

import serial

ser = None


def init_serial(port, baudrate):
    """ Open serial interface, if available """
    global ser
    try:
        ser = serial.Serial(port, baudrate)
        print "Opened serial port %s at %s" % (port, baudrate)
        ser.write("\n\nBEGIN TYR-VISION\n\n")
    except:
        print "Couldn't open serial port!"


# TODO: ser should not be passed to this function!
def send_data(*data):
    """
    Takes a list of data to send and sends it over serial in a comma
    separated list. Each data element in a packet is separated by a tab, and each
    packet is separated by a linefeed.

    Example: If the displacement vector is <-210, 42> then we send:
    -210\t42\n

    """
    if ser != None:
        string = ""
        for i in range(0, len(data)):
            string += str(data[i]) + "\t"
        string = string[:-2] # Remove trailing ', '
        string += '\r\n'  # linefeed at end of line
        #print string,  # print without an extra linefeed
        ser.write(string)
