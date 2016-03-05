# tyr-vision #
2016 Stronghold Vision Program

## Introduction ##
TO DO

## Dependencies ##
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


## Usage ##
Download the input video files [from Dropbox](https://www.dropbox.com/sh/1xdh4bo3m2r44cl/AADcpEpU6wbIWlsZE-8VSQ5Wa?dl=0).  
To run the program in a shell: `./tyr-vision.py`  
To pause/resume the program, press the spacebar.  
To exit the program, press the 'q' key. Note that the program cannot be exited in this way while it is paused.  


#### Flags ####
* `--show` or `-s` - Show the processed video on-screen.
* `--save` or `-S` - Save the processed video to disk. The file will be a timestamped AVI in the current directory. 
* `--fps` - Print the fps, average fps for the last 10 frames, and total average fps to the console.
* `--device` - Set the device to pull the video from. An integer X specifies the camera address `/dev/videoX` while anything else refers to the filepath of a video file. 
* `--port` - Set the location of the serial port (should be of the form `/dev/tty`*)
* `--baudrate` - Set the baudrate (bits per second)

#### Default Settings ####
* port = /dev/ttyTHS0
* baudrate = 9600
* device is [mini-field.mp4](https://www.dropbox.com/s/z4gh4nsmbl6pzyc/mini-field.mp4?dl=0)
* show_video = False
* save_video = False

#### Example usage: ####
`./tyr-vision.py -s`  
Use the default video file (mini-field.mp4) and show the processed video on screen. Good for developmental purposes. 
 
`./tyr-vision.py --device 0 -S`  
Use the default webcam (`/dev/video0`) and save the video to disk without showing it on-screen. Good for running on the Jetson. 

## Results ##
[Playlist on Youtube](http://www.youtube.com/playlist?list=PLRIAJ56nT-bs2UAK4jDW1Q4QOiR2Pfb30&jct=H55e7pyoEvJ9V2XWiWF1_fpI3wUWYA)
