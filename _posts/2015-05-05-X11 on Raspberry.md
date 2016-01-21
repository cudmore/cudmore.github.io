---
layout: post
title: "X11 on raspberry"
category: post
date: 2015-05-05 22:01:06
tags:
- linux
- raspberry
- osx
---

This is how I set up X11 on Raspberry server to serve individual windows to a Mac OSX client.

Any program you run on the Pi server that has a GUI should be piped to the display of your mac client.

####Install XQuartz on OSX

 - Install stalls at about 80%, be patient
 - Requires logout and login
 - Download [here][1]

####ssh to Raspberry using '-X'

    ssh -X pi@10.16.79.145
    
####On Raspberry server

 - This allows 'sudo python' to work with things like Tk()

        sudo cp ~/.Xauthority ~root/
    
 - This tells X11 on the Pi server to send its windows to your mac client (when you remote ssh with -X)
 
        export DISPLAY="127.0.0.1:10.0"
    
####Check that xeyes works
 - install

        sudo apt-get install x11-apps

 - run

        xeyes&
        xclock&
        leafpad&
    
####If this doesn't work

- open up X11 to everybody

        xhost +

####Run Arduino ide

    /usr/bin/arduino&
    
[1]: http://xquartz.macosforge.org/landing/
