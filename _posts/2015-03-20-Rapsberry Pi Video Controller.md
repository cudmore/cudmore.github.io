---
layout: post
title: "Raspberry-Pi-video-controller"
category: post
date: 2015-03-20 22:01:06
tags:
- raspberry pi
---

This post covers downloading, installing and running mjp-streamer on a raspberry pi. There are two options for installation and streaming depending on if you stream from (1) a rapsberry pi camera module or (2) a USB camera.

- Sourcecode for mjpg-streamer  
    [http://sourceforge.net/projects/mjpg-streamer/](http://sourceforge.net/projects/mjpg-streamer/)

- Tutorials  

    In what follows I am following this blog post ...
    [http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi](http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi)

    This post is derived from previous link but explains how to install a USB webcam instead of raspberry pi camera module ...
    [http://jacobsalmela.com/raspberry-pi-webcam-using-mjpg-streamer-over-internet/](http://jacobsalmela.com/raspberry-pi-webcam-using-mjpg-streamer-over-internet/)

###Install mjpg streamer

- Preliminaries  

	```bash
	sudo apt-get update  
	sudo apt-get upgrade  
	```
    
- Install dependencies

    ```bash
    sudo apt-get install libjpeg8-dev imagemagick libv4l-dev
    ```
    
- make symbolic link to changed library names. Thanks to Miguel Grinberg for [this](http://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi])
    
    ```bash
    ln -s /usr/include/linux/videodev2.h /usr/include/linux/videodev.h
    ```
    
- download mjpg-streamer

    ```bash
    wget http://sourceforge.net/code-snapshots/svn/m/mj/mjpg-streamer/code/mjpg-streamer-code-182.zip
    ```
    
- unzip

    ```bash
    unzip mjpg-streamer-code-182.zip  
    ```
    
####Here is where the installation differs depending on if you are installing (1) a usb camera or (2) the raspberry pi camera module

###(1) Raspberry Pi camera module
- build and install for raspberry pi camera module.  

    ```bash
    #build with 'make'
    cd mjpg-streamer-code-182/mjpg-streamer  
    make mjpg_streamer input_file.so output_http.so  
    #install by copying files
    sudo cp mjpg_streamer /usr/local/bin  
    sudo cp output_http.so input_file.so /usr/local/lib/  
    sudo cp -R www /usr/local/www      
    ```
  
    FOR COMPARISON, HERE IS SAME FOR USB CAMERA. IMPORTANT THING HERE IS '**input_uvc.so**'.
    
    ```bash
    #build with 'make'
    cd mjpg-streamer
    make mjpg_streamer input_file.so input_uvc.so output_http.so
    #install by copying
    sudo cp mjpg_streamer /usr/local/bin
    sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/
    sudo cp -R www /usr/local/www
    ```
  
    I GUESS YOU COULD JUST FOLLOW 'USB CAMERA' AND IT WOULD WORK FOR BOTH
    
- start the raspberry pi camera module

    ```bash
    mkdir /tmp/stream  
    raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 -th 0:0:0 &  
    ```
    
- start mjpg-streamer for raspberry pi camera module. This streams using '**input_file.so**'

    ```bash
    LD_LIBRARY_PATH=/usr/local/lib  
    mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www"
    ```
    
### (2) build for usb camera

- Plug in usb camera and verify it is automatically identified using 'lsusb'. If it is not you need to get a different camera or go down the rabbit-hole of installing linux drivers (beyond the scope of this post).  

	```bash
	pi@pi50 ~ $ lsusb  
	Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp.  
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub  
	Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.  
	Bus 001 Device 004: ID 1a40:0201 Terminus Technology Inc. FE 2.1 7-port Hub  
	Bus 001 Device 005: ID 1415:2000 Nam Tai E&E Products Ltd. or OmniVision Technologies, Inc. Sony Playstation Eye  
    ```

    The last entry is my camera, a 'Sony Playstation Eye'.
    
- install v4l-utils (THESE ARE WRONG !!!!!!!!!!!!!!!!)
    
    Getting v4l2 on the raspberry is witchcraft, as of march 2015 it seems to be installed by default???
    > sudo apt-get install v4l2-utils
    > sudo apt-get install uv4l2 uv4l2-raspicam
    
- Check the parameters of our USB camera  
	
	```bash
	v4l2-ctl --list-formats  
	
	ioctl: VIDIOC_ENUM_FMT  
		Index       : 0  
		Type        : Video Capture  
		Pixel Format: 'YUYV'  
		Name        : YUYV  
    ```
    
    The YUYV is very important, I need to pass a -y option to jpg_streamer --input command. If you see MPEG you don't need this -y switch.

- Here are some other commands to learn about calling conventions. This one told me who to pass -y for YUYV to. 
     
    ```bash
    mjpg_streamer --input "input_uvc.so --help"
    # note, i am not showing the output here
    # important line in output is this:
    #  [-y | --yuv ]..........: enable YUYV format and disable MJPEG mode
    ```

- build and install for usb camera. Critical thing here is '**input_uvc.so**'

    ```bash
    #build with 'make'
    cd mjpg-streamer
    make mjpg_streamer input_file.so input_uvc.so output_http.so
    #install by copying
    sudo cp mjpg_streamer /usr/local/bin
    sudo cp output_http.so input_file.so input_uvc.so /usr/local/lib/
    sudo cp -R www /usr/local/www
    ```
    
- run mjpg-streamer to stream from usb camera
    
    My usb camera uses YUYV, thus the '-y'
    
    ```bash
    /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so -y" -o "/usr/local/lib/output_http.so -w /usr/local/www"
    ```

    If my camera used MJPEG instead of YUYV, the command is the same without the '-y'.
    
    ```bash
    /usr/local/bin/mjpg_streamer -i "/usr/local/lib/input_uvc.so" -o "/usr/local/lib/output_http.so -w /usr/local/www"
    ```
    
###
