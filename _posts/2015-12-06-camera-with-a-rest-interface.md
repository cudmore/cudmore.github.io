---
layout: post
title: "Camera with a REST interface"
category: post
date: 2015-12-06 22:01:06
tags:
- raspberry
- linux
- flask
---

I've written a few versions of this. In previous versions I would control everything from a Python prompt, or a complex flask app, or use DIO to trigger video.

In this version I am trying to keep it simple and starting/stopping video and timelapse images with a REST api.

VideoServer.py is using a circular stream such that when recording is started, it also saves 'pre-triggered' video before recording was started. It can also capture timelapse images while it is recording video. The Raspberry camera is very nice for these two features.

To test this out, I will have a motion sensor on another Pi send a REST command to start video when it senses motion.

 - VideoServer.py, controls the camera with the following interface:
   - startArm(), initializes the camera.
   - stopArm(), release the camera.
   - startVideo(), starts video recording.
   - stopVideo(), stops video recording
   - doTimelapse=1, starts acquiring timelapse images
   - doTimelapse=0, stops acquiring timelapse images
   
 - timelapse_app.py, starts a flask webserver which provides a REST api as a wrapper around VideoServer.py:
 
```
     http://192.168.1.12:5010/startarm
     http://192.168.1.12:5010/stoparm
     http://192.168.1.12:5010/startvideo
     http://192.168.1.12:5010/stopvideo
     http://192.168.1.12:5010/timelapseon
     http://192.168.1.12:5010/timelapseoff
     http://192.168.1.12:5010/lastimage
```

**To Do:** I still need to expose 'bufferSeconds' and 'stillinterval' to the REST API.

###Get the last timelapse image in a browser or with curl

```
#display in browser
http://192.168.1.12:5010/lastimage
#save from command line
curl -o http://192.168.1.12:5010/lastimage
```

###rsync the images and video to a remote host

Now I want to get the videos/images off the machine with the camera. There are more options than I can count but here are three:

 - Push the recorded video/images to another server from within Python/Flask. I've done this before with [Paramiko](http://www.paramiko.org) but have always had problems with the code hanging or exceptions thrown when a network connection is lost. 
 - Have another machine (also running flask) pull the images off the camera machine. This can be done with the /lastimage REST path. This requires the other machine to be running server code itself and to have some sort of timer.
 - Use **rsynch** on the machine running the camera to a push videos/images to a remote server and use **cron** to do this at a regular interval.

I will use rsynch to push the images to a remote server. Follow [this](http://troy.jdmz.net/rsync/index.html) for a really thorough explanation.

```
#assuming you have a folder 'securitycam' on remote host
rsync -avz /home/pi/video/20151206/ -e ssh cudmore@192.168.1.200:securitycam
```

Make sure you can [login to remote server](http://127.0.0.1:4000/post/2015/05/04/Auto-login-to-ssh-server/) without entering a password

```
add this
```

Run rsynch command every 10 minutes with crontab

```
crontab -e
```

```
*/10 * * * * /usr/bin/rsync -avz /home/pi/video/20151206/ -e ssh cudmore@192.168.1.200:securitycam
```

###Here is a gist with VideoServer.py and timelapse_app.py

<script src="https://gist.github.com/cudmore/c4ab92d288cfd1778be5.js"></script>
