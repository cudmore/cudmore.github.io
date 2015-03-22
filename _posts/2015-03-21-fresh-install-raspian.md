---
layout: post
title: "Fresh install of Raspian"
category: post
date: 2015-03-21 22:01:06
tags:
- raspberry pi
- raspian
---

This is the procedure I follow to install a fresh raspbian system on a Raspberry Pi.

###configure pi (text menu)

    sudo raspi-config
    
###update database

    sudo apt-get update
    
###update Userspace software

    sudo apt-get upgrade
    
###update firmware

    sudo rpi-update
    
###afp

    sudo apt-get install netatalk
    
###Unison

See my post [here](http://www.robertcudmore.org/blog/?p=168)

    sudo apt-get install unison
    #see link to set up auto authentication with rsa keys
    unison #run once to make /home/pi/.unison
    pico /home/pi/.unison/sites.prf    

    # This is contents of /home/pi/.unison/sites.prf
    # Unison preferences file
    root = /home/pi/Sites
    root = ssh://robertcu@robertcudmore.org/raspberry/Sites

    ignore = Name *.tif
    ignore = Name .AppleDouble
    ignore = Name .DS_Store
    ignore = Name *.DS_Store
    ignore = Name *.shtml
    ignore = Name *.htaccess

    # Be fast even on Windows
    #fastcheck = yes

    servercmd=/home1/robertcu/unison

###Startup mailer
See my post [here](http://www.robertcudmore.org/blog/?p=60).

Use gmail 'cudmore.raspberry@gmail.com' to send  
    
     wget http://cudmore.github.io/downloads/startup_mailer.py

###What is my ip

Download whatismyip.py, run it and it will tell you your ip

    WOOPS, NOT THIS ... wget http://cudmore.github.io/downloads/startup_mailer.py
    
###python

    sudo apt-get install python-dev  
    
###pip

    sudo apt-get install python-pip  
    
###flask
tutorial: http://mattrichardson.com/Raspberry-Pi-Flask/

    sudo pip install flask  
    
- socketio: https://flask-socketio.readthedocs.org/en/latest/  
tutorial: http://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent

    sudo pip install flask-socketio  
    
####pandas (this takes awhile)

    sudo apt-get install python-pandas  
    
####mjpg-streamer  

See my post [here](http://cudmore.github.io/post/2015/03/15/Installing-mjpg-streamer-on-a-raspberry-pi/)

    sudo apt-get -y install libjpeg8-dev imagemagick libv4l-dev  
    sudo ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h  
    wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip  
    unzip mjpg-streamer-code-182.zip  
    cd mjpg-streamer-code-182/mjpg-streamer  
    make mjpg_streamer input_file.so input_uvc.so output_http.so  
    sudo cp mjpg_streamer /usr/local/bin  
    sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/  
    sudo cp -R www /usr/local/www  
    
    sudo apt-get install v4l-utils #this is to detect parameters of USB camera
    
Note, make input_uvc.so is for usb cam and input_file is for raspberry CSI camera

If wget does not find mjpg-streamer, download it here
    
    wget http://cudmore.github.io/downloads/mjpg-streamer-code-182.zip
    
####opencv

    sudo apt-get install libopencv-dev python-opencv
    
See my post on open cv []here]()http://cudmore.github.io/post/2015/03/07/use-opencv-to-acquire-video/)

# !!! Stop Here !!!

###Client side socket.io javascript
Client side needs socketio javascript: http://socket.io  
Put this in your Flask project /static/js/  
Something like /home/pi/Sites/iosserver/static/js/socket.io.min.js  

> wget https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.5/socket.io.min.js  
> cp socket.io.min.js Sites/iosserver/static/js/


###Client side jquery
documentation at: http://jquery.com/download/  

> wget wget http://code.jquery.com/jquery-1.11.2.min.js  
> cp jquery-1.11.2.min.js Sites/iosserver/static/js/


###miniconda
anaconda install tutorial http://docs.continuum.io/anaconda/install.html

> wget http://repo.continuum.io/miniconda/Miniconda-3.5.5-Linux-armv6l.sh
> bash Miniconda-3.5.5-Linux-armv6l.sh

> conda update conda
> conda update anaconda

###bokeh
bokeh quickstart: http://bokeh.pydata.org/en/latest/docs/quickstart.html
make sure dependencies are installed: NumPy, Pandas, and Redis
> pip install bokeh

###Streaming from a webcam or camera module using mjpg streamer

My home usb video camera shows up as

	pi@pi50 ~/Sites/iosserver $ lsusb
	Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp. 
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. 
	Bus 001 Device 004: ID 1a40:0201 Terminus Technology Inc. FE 2.1 7-port Hub
	Bus 001 Device 005: ID 1415:2000 Nam Tai E&E Products Ltd. or OmniVision Technologies, Inc. Sony Playstation Eye

Source code for mjpg streamer

http://sourceforge.net/projects/mjpg-streamer/

Tutorials

http://jacobsalmela.com/raspberry-pi-webcam-using-mjpg-streamer-over-internet/

http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi

#STREAMING HEADACHES

echo "`date +%y/%m/%d_%H:%M:%S`: stream_start" # 1>>/home/pi/stream.log

#old, for raspberry camera module
#sudo raspistill -w 640 -h 480 -q 5 -o /home/pi/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 -n >>/home/pi/stream.log 2>>/dev/null &
#export LD_LIBRARY_PATH=/home/pi/mjpg-streamer/
#mjpg-streamer/mjpg_streamer -i "input_file.so -f /home/pi/stream -n pic.jpg" -o "output_http.so -p 9000 -w /home/pi/mjpg-streamer/www" 0>>/home/pi/stream.log 1>>/home/pi/stream.log 2>>/home/pi/stream.log &

#new, march 2015
#/usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg"-o "output_http.so -w /usr/local/www"
#sudo /usr/local/bin/mjpg_streamer -i "./input_file.so -f /tmp/stream -n pic.jpg"-o "./output_http.so -w /usr/local/www"
export LD_LIBRARY_PATH=/home/pi/mjpg-streamer/
/usr/local/bin/mjpg_streamer -i "/home/pi/mjpg-streamer/input_file.so -f /tmp/stream -n pic.jpg" -o "/home/pi/mjpg-streamer/output_http.so -w /usr/local/www"

#this is off my website
#export LD_LIBRARY_PATH=/home/pi/mjpg-streamer/
#mjpg-streamer/mjpg_streamer -i "input_file.so -f /home/pi/stream -n pic.jpg" -o "output_http.so -p 9000 -w /home/pi/mjpg-streamer/www" &

#1
LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"
#2
/usr/local/bin/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"
/usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so" -o "/usr/local/lib/output_http.so -w /usr/local/www"

myip=$(hostname -I)

myip=$(echo -n $myip)

echo "View the stream in VLC with"
echo "   http://$myip:9000/?action=stream"

###my usb webcam has following output
- v4l2-ctl --list-formats
	pi@pi50 ~ $ v4l2-ctl --list-formats
	ioctl: VIDIOC_ENUM_FMT
		Index       : 0
		Type        : Video Capture
		Pixel Format: 'YUYV'
		Name        : YUYV

- v4l2-ctl --list-ctrls
	pi@pi50 ~ $ v4l2-ctl --list-ctrls

	User Controls

						 brightness (int)    : min=0 max=255 step=1 default=0 value=0 flags=slider
						   contrast (int)    : min=0 max=255 step=1 default=32 value=32 flags=slider
						 saturation (int)    : min=0 max=255 step=1 default=64 value=64 flags=slider
								hue (int)    : min=-90 max=90 step=1 default=0 value=0 flags=slider
			white_balance_automatic (bool)   : default=1 value=1
						   exposure (int)    : min=0 max=255 step=1 default=120 value=120 flags=inactive, volatile
					 gain_automatic (bool)   : default=1 value=1 flags=update
							   gain (int)    : min=0 max=63 step=1 default=20 value=20 flags=inactive, volatile
					horizontal_flip (bool)   : default=0 value=0
					  vertical_flip (bool)   : default=0 value=0
			   power_line_frequency (menu)   : min=0 max=1 default=0 value=0
						  sharpness (int)    : min=0 max=63 step=1 default=0 value=0 flags=slider

	Camera Controls

					  auto_exposure (menu)   : min=0 max=1 default=0 value=0 flags=update

-mjpg_streamer --input "input_uvc.so --help"
	pi@pi50 ~ $ mjpg_streamer --input "input_uvc.so --help"
	MJPG Streamer Version: svn rev: Unversioned directory
	 ---------------------------------------------------------------
	 Help for input plugin..: UVC webcam grabber
	 ---------------------------------------------------------------
	 The following parameters can be passed to this plugin:

	 [-d | --device ].......: video device to open (your camera)
	 [-r | --resolution ]...: the resolution of the video device,
							  can be one of the following strings:
							  QSIF QCIF CGA QVGA CIF VGA 
							  SVGA XGA SXGA 
							  or a custom value like the following
							  example: 640x480
	 [-f | --fps ]..........: frames per second
	 [-y | --yuv ]..........: enable YUYV format and disable MJPEG mode
	 [-q | --quality ]......: JPEG compression quality in percent 
							  (activates YUYV format, disables MJPEG)
	 [-m | --minimum_size ].: drop frames smaller then this limit, useful
							  if the webcam produces small-sized garbage frames
							  may happen under low light conditions
	 [-n | --no_dynctrl ]...: do not initalize dynctrls of Linux-UVC driver
	 [-l | --led ]..........: switch the LED "on", "off", let it "blink" or leave
							  it up to the driver using the value "auto"
	 ---------------------------------------------------------------

	input_init() return value signals to exit

#THIS WORKS FOR USB WEBCAM
/usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -y" -o "/usr/local/lib/output_http.so -w /usr/local/www"

> /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -y" -o "/usr/local/lib/output_http.so -w /usr/local/www"
- /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -y" -o "/usr/local/lib/output_http.so -w /usr/local/www"
