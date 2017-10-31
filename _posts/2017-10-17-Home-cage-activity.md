---
layout: post
title: "Home Cage Activity"
category: post
date: 2017-10-17 00:00:01
tags:
- analysis
---

Record video 24/7 with a Raspberry Pi

The parts list and implementation details are in [the original blog post][1].

## The Raspberry Pi is running Debian Linux and is networked

	IP: 10.16.80.162
	username: pi
	password: 

### To login to the Pi

On Windows, download and then use Putty

On OSX, use the terminal application in `/Applications/Utilities/Terminal.app` and type:

    ssh pi@10.16.80.162


### Logout of the Pi
    exit

### Mount the pi hard-drive as a file-server

On Windows, in the start menu, type:

    \\10.16.80.162

On OSX, ‘Connect to Server...’ and type:

    afp://10.16.80.162
    or
    smb://10.16.80.162

### Saved files

File are saved in `/home/pi/video/`


## Super simplified

 Login to the pi and there are three commands
 
 **start** : Start lights and video
 **stop** : Stop lights and video
 **running** : Tells you if the lights/video are running
 
## Running the code

Run **lights.py** to control the lights

    screen
    cd /home/pi/Sites/homecage
    python lights.py
    #exit screen with ctrl+a then d
    exit 

Run **video.py** to record video

    screen
    cd /home/pi/Sites/homecage
    python video.py
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


## Converting .h264 files to .mp4

Video files in .h264 need to be converted to .mp4 so they have meaningful fps. Do this with a bash script on osx.

 - Put the following code into a text file named `convert.sh` in same folder as .h264 files.

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
 - ./convert.sh
 
 **convert.sh** will make an mp4/ folder with .mp4 copies of all your video files

## To start over

The following sequence will start the video recording and lights again

    1) pull power and plug back in
    2) login with putty/terminal
    3) cd Sites/homecage
    4) screen
    5) python lights.py
    6) [exit screen with ctrl+a then d]
    7) screen
    8) python video.py
    9) [exit screen with ctrl+a then d]
    10) exit

## The source code for lights.py and video.py

<script src="https://gist.github.com/cudmore/576a808108acf22ff0a259cc1fc30c2a.js"></script>
[1]: /post/2014/02/14/Monitoring-mice-in-their-home-cage/

## History

This was originally written as readme for Valerie in the Bergles lab, 20160723.
