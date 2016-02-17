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
import random


""" DEFAULT SETTINGS """
port='/dev/ttyUSB0'
baudrate=9600
delay = 0.03
dry = False
loopback = False
garbage_mode = None
output_counter = 0  # number of times that output() has been called


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


def data_generator():
    """
    Generates a string in the format x\ty\n
    where x increasing from 0 to 100 and y corresponding decreases from 100 to 0.
    """
    k = output_counter%100
    text = "%s\t%s\n" % (k, 100 - k)
    return text


def garbage_generator(mode):
    """ Returns a random string after waiting for a random delay """
    if mode == 0: # alternate between all 4 garbage modes
        j = output_counter % 4 + 1
    else:
        j = mode

    if j == 1:  # legit data
        text = data_generator()
    elif j == 2:  # missing linefeed
        text = data_generator().rstrip("\n")
    elif j == 3:  # Letters instead of numbers, tab-separated
        text = "asdf\thjkl\n"
    elif j == 4:  # random binary data
        text = ''.join([chr(random.randint(0,255)) for i in xrange(20)]) + "\n"
    return text


def output(text):
    """
    Output the given text.
    If dry mode is enabled, simply print it to the console.
    Otherwise, write to the serial port. If the serial port is a virtual
    loopback, then also print from the master pty.
    """
    global output_counter
    output_counter += 1  # increment counter for number of times output has been called
    if dry:
        print text,
    else:
        ser.write(text)
        if loopback:  # Note: loopback buffer is not flushed until \n is sent or user exits with ^C
            print os.read(master, 1000),


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
    elif flag == "--garbage":
        # Enable garbage output mode
        i += 1
        garbage_mode = int(sys.argv[i])


""" Print the settings """
print "Port: %s" % port
print "Baudrate: %s" % baudrate
print "Delay: %s" % delay
if dry:
    print "Dry mode enabled!"
if loopback:
    print "Loopback mode enabled!"
if garbage_mode:
    print "Garbage mode enabled!"


# Setup serial if we're not in dry mode
if dry == False:
    try:
        ser = serial.Serial(port, baudrate)
    except:
        print "Couldn't open serial interface! Running in dry mode."
        dry = True


""" Main program loop """
while 1:
    try:
        if garbage_mode is None:
            text = data_generator()
        else:
            text = garbage_generator(garbage_mode)

        output(text)
        time.sleep(delay)
    except KeyboardInterrupt:
        print "Exiting..."
        ser.close()
        sys.exit()


# TODO: write a unit test
