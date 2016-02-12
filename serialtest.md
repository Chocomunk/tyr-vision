# serialtest
Author: William Meng

This program is used for testing output to serial interfaces.  
It outputs ASCII data in the form `x\ty\n` where `x` goes from 0 to 100 and `y` goes from 100 to 0.  
The `\t` is the ASCII tab character, and the `\n` is the ASCII line feed character. 

## Usage ##
Run the program: `./serialtest.py`

#### Flags ####
* `--port` Specify the serial port.
* `--baudrate` Specify the baudrate (bitrate).
* `--delay` Specify the delay between consecutive outputs, in seconds. 
* `--dry` Enable dry mode. Print to the console instead of using a serial port. 
* `--loopback` Open a virtual serial interface for loopback testing. Outputs will be printed by reading from the master pty. 

#### Default Options ####
* port = /dev/ttyUSB0
* baudrate = 9600
* delay = 0.03
* dry = False

Example usage:  
`./serialtest.py --delay 0.1 --loopback`  
Opens a loopback interface and outputs every 0.1 seconds. 

`./serialtest.py --port /dev/ttyTHS0`  
Opens /dev/ttyTHS0 at 9600 baud, outputs every 0.03 seconds. Good for testing the primary 18V UART on the Jetson TK1. 
