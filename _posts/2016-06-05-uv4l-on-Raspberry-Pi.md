---
layout: post
title: "uv4l on Raspberry Pi"
category: post
date: 2016-06-05 01:01:06
tags:
- raspberry
- debian
- linux
- video
---

The uv4l people have update their code and you can now stream real-time high resolution video to a browser. And it works on the Raspberry Pi. The 'u' in uv4l is for 'user'. It is a user-space wrapper around the low-level kernel driver [v4l][v4l]. It is just a matter of time before the people making v4l put the finishing touches on it and it will come standard on linux distributions. On the Raspberry Pi, work is underway on [v4l2][v4l2].

This software has a lot of aspirations beyond video including implementing all sorts of real-time web communication with [webRTC][webrtc]. 

As of Nov 2017, following [this tutorial][1].

## Determine which version of Raspbian you are running.


```
cat /etc/os-release
```

```
PRETTY_NAME="Raspbian GNU/Linux 8 (jessie)"
NAME="Raspbian GNU/Linux"
VERSION_ID="8"
VERSION="8 (jessie)"
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
```

## Add apt key

### Wheezy or Jessie

	curl http://www.linux-projects.org/listing/uv4l_repo/lrkey.asc | sudo apt-key add -
	
### Stretch

	curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -


## Add the following to '/etc/apt/sources.list'

Edit the file with `sudo pico /etc/apt/sources.list`

### Wheezy

	deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ wheezy main

### Jessie

	deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/ jessie main

### Stretch

	deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main
	
## Install uv4l

	sudo apt-get update #update database
	sudo apt-get upgrade #update userspace
	sudo apt-get install uv4l uv4l-raspicam uv4l-server
	
## Starting and stopping uv4l streaming

### Run driver

    uv4l --driver raspicam --auto-video_nr --width 640 --height 480 --encoding jpeg
    
### Kill

    pkill uv4l

### Run a streaming server with real-time video streaming

	uv4l --driver raspicam --auto-video_nr --encoding h264 --width 640 --height 480 --enable-server on

This runs a web server on port 8080. Once running, browse to your machines IP. The stream should have almost 0 lag time and be running at about 30 fps. Amazing.

	http://192.168.1.60:8080
	
## Troubleshooting


  
See Also

 - [Use cases](http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=16#example11)
    
[v4l]: https://www.linuxtv.org
[v4l2]: https://www.raspberrypi.org/forums/viewtopic.php?t=62364
[webrtc]: https://webrtc.org
[1]: https://www.linux-projects.org/uv4l/installation/