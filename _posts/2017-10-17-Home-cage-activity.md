---
layout: post
title: "Home Cage Activity"
category: post
date: 2017-10-17 00:00:01
tags:
- analysis
---

This was originally written as readme for Valerie in the Bergles lab, 20160723

IP: 10.16.79.93
username: pi
password: raspberry


## Mount the pi hard-drive as a file-server

    On Windows, in the start menu, type
    \\10.16.79.93

    On OSX, in the ‘Coonect to Server...’ dialog, type:
    afp://10.16.79.93


## To Login to the Pi on Windows

Download and then use Putty


## To Login to the Pi on OSX

Use terminal and then type:

    ssh pi@10.16.79.93


### Logout of the Pi
    exit


## Running the code

### Run the code inside of **screen**

Run testhome.py to control the lights

    screen
    cd /home/pi/homecageactivity
    python testhome.py
    #exit screen with ctrl+a then d
    exit 

Run video.py to record video

    screen
    cd /home/pi/homecageactivity
    python testhome.py
    #exit screen with ctrl+a then d
    exit 

Both programs need to be run inside a screen session. This way when your ssh session logs out, the programs will continue to run. If you do not run these programs within a screen session, the programs will stop recording when you log out.

To exit screen mode, hold down 'ctrl' and then 'a' key at the same time. Let go of 'ctrl' and 'a' keys. Then press 'd' key

### To return to a screen session

1) List the sessions with 'screen -r'

    screen -r
    ~/homecageactivity $ screen -r
    There are several suitable screens on:
	  1255.pts-5.homecage	(07/20/2016 04:41:04 PM)	(Detached)
	  1186.pts-1.homecage	(07/20/2016 04:40:06 PM)	(Detached)
    Type "screen [-d] -r [pid.]tty.host" to resume one of them.

2) Return to a particular screen with

    screen -r 1255.pts-5.homecage

Or

    screen -r 1186.pts-1.homecage
    

### To stop a program

Return to its screen (with screen -r ...) and press ctrl+c


## Saved files

File are saved in

    /home/pi/video/

Video files in .h264 need to be converted to .mp4 so they have meaningful fps. Do this with a bash script on osx.

 - Put the following code into a text file named convert.sh in same folder as .h264 files

```bash
	mkdir mp4

	for file in *.h264 ; do
		filename="${file%.*}"
		echo $filename
		ffmpeg -r 15 -i "$file" -vcodec copy "mp4/$file.mp4"
		sleep 3
	done
```
	
 - chmod +x convert.sh
 - ./convert.sh will make a new mp4 directory with all your video files

## To start over

The following sequence will start the video recording and lights again

    1) pull power and plug back in
    2) login with putty/terminal
    3) cd /homecageactivity
    4) screen
    5) python testhome.py
    6) [exit screen with ctrl+a then d]
    7) screen
    8) python video.py
    9) [exit screen with ctrl+a then d]
    10) exit