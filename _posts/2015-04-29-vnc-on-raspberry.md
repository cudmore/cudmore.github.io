---
layout: post
title: "VNC on raspberry pi"
category: post
date: 2015-04-29 22:01:06
tags:
- raspberry
---

###Remote login to Raspberry with tightvnc

See

    https://www.raspberrypi.org/documentation/remote-access/vnc/
    http://elinux.org/RPi_VNC_Server

###Install tightvncserver server on Raspberry

    sudo apt-get install tightvncserver

###Run tightvncserver to set password

    tightvncserver

###Start server on pi

Use :1 if your Pi is running X11 by default (mine is)

    vncserver :1 -geometry 1920x1080 -depth 24
    vncserver :1 -geometry 1280x800 -depth 24
    vncserver :1 -geometry 1024x768 -depth 24

###kill server

    vncserver -kill :1

###Install realVNC client on OSX

    https://www.realvnc.com

###Enable copy/paste between host and server

See
    
http://raspberrypi.stackexchange.com/questions/4474/tightvnc-copy-paste-between-local-os-and-raspberry-pi


    # install
    sudo apt-get install autocutsel
    
    #edit /home/pi/.vnc/xstartup
    pico .vnc/xstartup 
    
    #make it look like this
    #!/bin/sh

    xrdb $HOME/.Xresources
    xsetroot -solid grey
    #added 20150414 to get copy paste to work
    autocutsel -fork
    #x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
    #x-window-manager &
    # Fix to make GNOME work
    export XKL_XMODMAP_DISABLE=1
    /etc/X11/Xsession

###Alternative is to use x11vnc

See

https://www.raspberrypi.org/forums/viewtopic.php?p=108862

https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=19600

####Pros
- This will 'recycle' your :0 display if you are booting with X11
- You will be able to see the same screen on direct HDMI/Video output and your remote connection simultaneously
- You will remote login (with realVNC) and get the same desktop
- Copy/Paste works by default

####Cons
- This would work if you always had a HDMI display at a desired resolution (or tweaked /boot/config.txt to force HDMI).
- Does not work well if you are throwing your display out an analog RCA jack, it is too low res and then your VNC connection just follows that low resolution. Maybe could fix this?

