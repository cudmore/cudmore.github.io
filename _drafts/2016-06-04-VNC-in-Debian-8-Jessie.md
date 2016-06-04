---
layout: post
title: "VNC in Debian 8 Jessie"
category: post
date: 2016-06-04 01:01:06
tags:
- debian
- linux
---

Debian 8 Jessie will not run vnc using the gnome desktop. This bug will not be fixed until Debian 9.

Solution is to either use KDE or [Mate](http://mate-desktop.com) desktops. Mate is a fork of Gnome.

- Uninstall Gnome

    apt-get remove gnome-core
    
- [Install Mate](http://wiki.mate-desktop.org/download)

    sudo apt-get update
    sudo apt-get install mate-desktop-environment-extras

- Reconfigure xstartup

Following [this](https://forums.linuxmint.com/viewtopic.php?t=99225) discussion.

    pico /home/cudmore/.vnc/xstartup
    
	#!/bin/sh

	# Uncomment the following two lines for normal desktop:
	#unset SESSION_MANAGER
	unset DBUS_SESSION_BUS_ADDRESS
	#. /etc/X11/xinit/xinitrc
	#/usr/bin/mate-session

	[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
	[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
	xsetroot -solid grey
	vncconfig -iconic &
	x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
	mate-session &

- Restart VNC

	vncserver -kill :1 # shutdown if neccessary
	vncserver :1
	
- Login from a remote machine

On OS X, use [VNC Viewer](https://www.realvnc.com/download/viewer/) from realvnc
