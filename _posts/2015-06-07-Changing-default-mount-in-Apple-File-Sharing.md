---
layout: post
title: "Changing default mount name in Apple File Sharing"
category: post
date: 2015-06-07 22:01:06
tags:
- linux
- raspberry pi
---

I mount multiple Raspberry Pi's via Apple File Protocol (AFP). They each get mounted on my Mac as a hard-drive on the desktop but each one defaults to the same name 'Home Directory'. There is no way to tell them apart once mounted (except for looking at what is in them).

Here is how you change the name of the default AFP mount point.

    #stop netatalk
    sudo /etc/init.d/netatalk stop
    
    #edit config file
    sudo nano /etc/netatalk/AppleVolumes.default
	
	#change this one line
	
	# By default all users have access to their home directories.
	#~/                     "Home Directory"
	~/                      "pi50"

    #restart netatalk
    sudo /etc/init.d/netatalk start

This pi will now mount on my Mac desktop as a hard-drive named 'pi50'

####Links

I got this [from here](https://www.raspberrypi.org/forums/viewtopic.php?f=36&t=26826).