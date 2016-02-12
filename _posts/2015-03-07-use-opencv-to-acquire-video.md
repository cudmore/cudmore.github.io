---
layout: post
title: "Use OpenCV to acquire video"
category: post
date: 2015-03-07 22:01:06
tags:
- data acquisition
---
#### Goals
- Use raspberry to record video from USB camera and stream to disk.
- Use python and opencv
- will save either as a sequence of .tif or as an uncompressed videofile
 
#### Install opencv
> sudo apt-get update  
> sudo apt-get upgrade  
> sudo apt-get install libopencv-dev python-opencv

- Remember that I have conda install of python in '/home/pi/miniconda/bin/python'.
- I need to use '/usr/bin/python' instead.

#### Check opencv install
    pi@pi40 ~ $ /usr/bin/python  
    Python 2.7.3 (default, Mar 18 2014, 05:13:23) 
    [GCC 4.6.3] on linux2  
    Type "help", "copyright", "credits" or "license" for more information.  
    >>> import cv2  
    >>> cv2.__version__  
    '2.4.1'

#### Install USB thumb drive + usb camera
- after pluggin in usb drive + usb camera
    
    pi@pi40 ~ $ lsusb  
    Bus 001 Device 002: ID 0424:9512 Standard Microsystems Corp. 
    Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub  
    Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp. 
    Bus 001 Device 005: ID 1415:2000 Nam Tai E&E Products Ltd. or OmniVision Technologies, Inc. Sony Playstation Eye  
    Bus 001 Device 004: ID 13fe:4100 Kingston Technology Company Inc.  
    
#### Got some python/opencv code to acquire
- Acquires individual .tif files in a loop

#### To do
- Check the frame rate by recording a clock
- Add in template code for stop/start, start with keyboard and then move to GPIO
- Get the DC60 STK1160 video to usb dongle working
- This website says that it may just auto detect in newer linux kernels?
http://linuxtv.org/wiki/index.php/Stk1160# Making_it_Work

#### Here is the code

	#/usr/bin/python

	import numpy as np
	import cv2

	# initialize camera
	cap = cv2.VideoCapture(0)
	if cap is None:
	    print 'Warning: unable to access camera'

	# stopPin = 7 # listen for a change on this pin to stop

	# number of frames to acquire
	numFrames = 30
	currFrame = 0

	# outfilebase = 'images/image' # append number + .tif

	print 'starting capture of ' + str(numFrames) + ' frames.'
	print 'press ctrl-c to stop ... eventually we will stop on a TTL'
	while(cap.isOpened()):
	    try:
	        ret, frame = cap.read()
	        if ret==True:
	            # flip frame
	            # frame = cv2.flip(frame,0)

	            # print frame.shape

	            # write the flipped frame
	            try:
	                # out.write(frame)
	                # cv2.SaveImage('file' + str(currFrame) + '.tif', frame)
	                cv2.imwrite('images/image' + str(currFrame) + '.tif', frame)
	            except:
	                print 'Error in out.write() OR user hit ctrl-c'
	                break

	            currFrame += 1
	            # if (currFrame > numFrames):
	            #    print 'finished ' + str(numFrames) + ' frames.'
	            #    break
	    
	        else:
	            break

	    except KeyboardInterrupt:
	        print 'user hit ctrl-c'
	        print 'frames=' + str(currFrame)
	        break

	# Release camera
	cap.release()


