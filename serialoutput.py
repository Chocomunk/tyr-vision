# serialoutput.py
#
# Module for serial output

# import serial

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


def serialize(data):
    """
    Formats given data into a string in a format suitable for sending it over
    the serial interface.

    Each data element is separated by a tab, and the line is
    terminated with a carriage return and linefeed.

    Example: If the data is (-210, 42, 61, 20) then it returns:
    "-210\t42\t61\t20\r\n"
    """
    string = ""
    for i in range(0, len(data)):
        string += str(data[i]) + "\t"

    string = string[:-2] # Remove trailing 2 characters, ie. '\t'
    string += '\r\n'  # add carriage return and linefeed
    #print string,  # print without an extra linefeed (for debugging)
    return string


def send_data(*data):
    """ Sends given data over serial. """
    string = serialize(data)
    if ser != None:
        #print string,  # print without an extra linefeed
        ser.write(string)


def close():
    """ Closes the serial interface """
    if ser is not None:
        ser.close()
