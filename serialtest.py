#!/usr/bin/env python2
#
# serialtest.py
#
# A program for testing serial connections
#

import time
import serial
import sys
import os, pty


""" DEFAULT SETTINGS """
port='/dev/ttyUSB0'
baudrate=9600
delay = 0.03
dry = False


def setup_loopback():
    """
    Sets up virtual serial ports for reading and writing data.
    Returns the name of the slave port and a descriptor of the master port.

    Virtual serial interfaces on Linux: http://stackoverflow.com/a/19733677
    Python version: http://stackoverflow.com/a/15095449
    """
    master, slave = pty.openpty()
    m_name = os.ttyname(master)
    s_name = os.ttyname(slave)
    print "Writing to slave port: %s" % s_name
    print "Reading from master port: %s" % m_name
    return s_name, master


""" PROCESS COMMAND LINE ARGUMENTS """
for i in range(1, len(sys.argv)):
    flag = sys.argv[i]
    if flag == "--port":
        i += 1
        port = sys.argv[i]
    elif flag == "--baudrate":
        i += 1
        baudrate = int(sys.argv[i])
    elif flag == "--delay":
        i += 1
        delay = float(sys.argv[i])
    elif flag == "--dry":
        dry = True
    elif flag == "--loopback":
        i += 1
        loopback = True
        port, master = setup_loopback()


""" Print the settings """
print "Port: %s" % port
print "Baudrate: %s" % baudrate
print "Delay: %s" % delay
if loopback:
    print "Loopback mode enabled!"


# Setup serial if we're not in dry mode
if dry == False:
    ser = serial.Serial(port, baudrate)


def output(text):
    """
    Output text. If dry mode is enabled, simply print it to the console.
    Otherwise, write to the serial port. If the serial port is a virtual
    loopback, then also read and print from the master pty.
    """
    if dry:
        print text,
    else:
        ser.write(text)
        if loopback:
            print os.read(master, 1000),


while 1:
    try:
        for x in range(0, 100):
            # first term counts up to 100, second term counts down from 100
            text = "%s\t%s\n" % (x, 100 - x)
            output(text)
            time.sleep(delay)
    except KeyboardInterrupt:
        print "Exiting..."
        ser.close()
        sys.exit()


# TODO: write a unit test
