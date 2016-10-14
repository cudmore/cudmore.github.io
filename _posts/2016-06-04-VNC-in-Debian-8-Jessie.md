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

- [UPDATE] 20160823 Installed cairo-dock

[See this](http://glx-dock.org/ww_page.php?p=From%20the%20repository&lang=en) (I copy/pasted text below)

Add this line to /etc/apt/sources.list (don't forget to replace #CODENAME# by stable/testing/unstable)

    deb http://download.tuxfamily.org/glxdock/repository/debian #CODENAME# cairo-dock ## Cairo-Dock Stable

Then, copy-paste all this box in a terminal of your Debian stable/testing/unstable

    su
    wget -q http://download.tuxfamily.org/glxdock/repository/cairo-dock.gpg -O- | apt-key add - 
    apt-get update 
    apt-get install cairo-dock cairo-dock-plug-ins

Force APT to use packages from our repository
It's recommended to force APT to use Cairo-Dock's packages from our repository instead of Cairo-Dock's packages from official Debian repositories (because the latter are poorly made with a lot of unnecessary dependencies). For that, simply create this file: /etc/apt/preferences.d/cairo-dock 
With this content:

    Package: cairo-dock* libgldi* 
    Pin: origin download.tuxfamily.org 
    Pin-Priority: 990

- Turn off default mate tray (the one at the bottom)

Right-click panel/tray and delete it

- Add to startup items

    /usr/bin/cairo-dock
    
    
