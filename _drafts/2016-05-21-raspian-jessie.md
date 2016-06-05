---
layout: post
title: "Installing Raspian Jessie on a Raspberry 2/3"
category: post
date: 2016-05-21 01:01:06
tags:
- raspberry
- linux
---

If you are Microsoft Windows based, have a look [here][mswindows] for a good install guide.

# Download image

As of May 21, 2016 the image was named `2016-05-10-raspbian-jessie`. [Download here][downloadraspian]

# Copy image to SD card

Follow an installation guide [here][installguide].

On Mac OS

    #Insert SD card and format as Fat32
	diskutil list # find the /dev/disk<n>, mine was /dev/disk3
	diskutil unmountDisk /dev/disk3 #unmount disk
	# copy .img file to disk
	sudo dd bs=1m if=/Users/cudmore/Downloads/2016-05-10-raspbian-jessie.img of=/dev/rdisk3

# First boot of the Pi

Connect Pi to a router with an ethernet cable and boot

Find IP address using router web interface, usually http://192.168.1.1

# Login via ssh

    ssh pi@192.168.1.15
    #password is raspberry
    
# Run configuration utility

    sudo raspi-config
  
 - 1 Expand Filesystem
 - 2 Change User Password
 - 3 Boot Options
   - B1 Console
 - 5 Internationalisation Options
   - I1 Change Local -> en_US.UTF-8 UTF-8
   - I2 Change Timezone -> US -> Eastern
   - I4 Change Wi-fi Country -> US United States
 - 6 Enable Camera
 - 9 Advanced Options
   - A2 Hostname -> [choose a name here, I chose pi3]
 - Set the network name with xxx
 - Turn on the camera
   
Selecting Boot Options -> Console is important. IT seems Raspbian ships with X-Windows on by default.

# Update the system

    sudo apt-get update  #update database
    sudo apt-get upgrade #update userspace
    sudo rpi-update      #update firmware (requires reboot)
    sudo reboot          #reboot

# AFP / Netatalk / Avahi

Once netatalk is installed, the Raspberry will show up in the Mac Finder 'Shared' section

    sudo apt-get install netatalk
    
[downloadraspian]: https://www.raspberrypi.org/downloads/
[installguide]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[mswindows]: http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/