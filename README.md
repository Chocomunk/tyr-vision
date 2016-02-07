# tyr-vision
2016 Vision

### Dependencies ###
Install the following system packages  

* Python 2
* pip
* python-opencv

On Debian/Ubuntu, run:  
`sudo apt-get install python python-pip python-opencv`  

On Arch Linux:   
`sudo pacman -S python2 python2-pip python2-numpy`  

Install the following python packages:

* numpy
* cv2

If you're using the system Python, run:  
`sudo pip install numpy cv2`


### Usage ###
Download the test video file [here](https://drive.google.com/open?id=0B3CtH7XCgLzOT0trdTlpc1c0UlE).  
To run the program in a shell: `./tyr-vision.py`  
To exit the program, press the 'q' key.

#### Flags ####
* `--show` or `-s` - Show the video feed
* `--save` or `-S` - Save the video feed
* `--device` - Set the device to pull the video from
* `--port` - Set the location of the serial port
* `--baudrate` - Set the baudrate
