---
layout: post
title: "Installing Raspian Stretch on a Raspberry Pi"
category: post
date: 2017-11-22 01:01:06
tags:
- raspberry
- linux
---

These are instructions for installing the Raspian Stretch (Debian) system on a Raspberry Pi.

## 1) Set up the SD card

You want a name brand `class 10` card with about 16 GB.

### 1.1) Download image

 [Download here][downloadraspian]

 - As of May 21, 2016 the image was named `2016-05-10-raspbian-jessie`.
 - As of Nov 16, 2017 the image was named `2017-09-07-raspbian-stretch-lite`.
 - As of April 19, 2018 the image was named `2018-04-18-raspbian-stretch-lite`.
 
### 1.2) Copy the downloaded image to SD card

If you run into trouble, follow this [installation guide][installguide]. 

#### On MacOS

Unzip the .zip file by right clicking the .zip file and selecting `Open With - Archive Utility.app (default)`. This will yield a .img file.

Insert an SD card and use `DiskUtil` to format it as Fat32. In OSX Sierra this is DiskUtil - Erase - Format as 'MS-DOS (FAT)'.

Use DiskUtil to 'unmount' the SD card (don't eject, you need to unmount)

Find the location of your SD card

```
# in a terminal, type
diskutil list
```

You should see something like this.

```
/dev/disk4 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *15.9 GB    disk4
   1:             Windows_FAT_32 NO NAME                 15.9 GB    disk4s1
```

Copy the .img file to the SD card. Assuming your SD card was listed as /dev/disk4

```bash
sudo dd bs=1m if=/Users/cudmore/Downloads/2017-09-07-raspbian-stretch-lite.img of=/dev/rdisk9
```

Note that this command requires `/dev/rdisk` rather than `/dev/disk`.

#### On Windows

Follow install guides [here][installguide].

### 1.3) Configure the Pi run ssh on boot

Raspbian usually has the SSH server disabled by default and it needs to be activated manually. To do this, create an empty file named `ssh` in the root folder of the SD card

On MacOS, open a terminal and type:

    touch /Volumes/boot/ssh
    
## 2) First boot of the Pi

Insert SD card into a Pi, connect Pi to a router with an ethernet cable and boot

Find IP address using router web interface, usually http://192.168.1.1

### 2.1) Login via ssh

#### On MacOS

In a terminal window, type the following, where `[piIP]` is address of your Pi you found in the previous step.

    ssh pi@[piIP]
    #password is raspberry

#### On Windows

Download and use [Putty][putty].
    
### 2.2) Run configuration utility

```
sudo raspi-config
```

The name and location of these options change as Raspbian gets updated. This is still the general idea

 - 1 Change User password
 - 2 Network Options - Configure network settings   
   - N1 Hostname - Set the visible name for this Pi on a network  
 - 3 Boot Options
   - B1 Desktop / CLI 
     - B1 Console
 - 4 Localization Options
   - I1 Change Local
     - De-Select en_GB.UTF-8 UTF-8
     - Select en_US.UTF-8 UTF-8 
   - I2 Change Timezone
   - I4 Change Wi-fi Country
 - 5 Interface Options
   - P1 Camera
 - 7 Advanced Options
   - A1 Expand Filesystem
     
Selecting `3 Boot Options -> B1 Console` is important. It seems Raspbian ships with a GUI desktop on by default and you want to turn it off.

Here, I am setting my locale to en_US.UTF-8. If you are in a different country you should set this as you want.

### 2.3) Update the system

    sudo apt-get update  #update database
    sudo apt-get upgrade #update userspace (this can take a long time)
    sudo reboot          #reboot

## Checking your Raspian, hardware, and firmware

Checking your Raspian version

	cat /etc/os-release
	
Returns

	PRETTY_NAME="Raspbian GNU/Linux 9 (stretch)"
	NAME="Raspbian GNU/Linux"
	VERSION_ID="9"
	VERSION="9 (stretch)"
	ID=raspbian
	ID_LIKE=debian

Checking your Raspberry Pi version (the hardware)

	cat /proc/device-tree/model
	
Returns

	Raspberry Pi 3 Model B Rev 1.2

Checking your firmware (pretty cryptic)

	uname -a

Returns

	Linux pi_bplus 4.14.34+ #1110 Mon Apr 16 14:51:42 BST 2018 armv6l GNU/Linux

## Setup the network

If you are connecting to a local router there is no additional setup required.

When on a university network (At least the Hopkins network), it is strongly suggested to use hard wiring with an ethernet cable rather than relying on wifi. Ask your network administrator to authenticate based on the MAC address of the Raspberry Ethernet port. You can find this with:

```
ifconfig eth0
```
	
Which returns something like this, telling us the MAC address is `b8:27:eb:aa:51:6d`

```
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.5  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::303f:6054:3ec9:3bfb  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:aa:51:6d  txqueuelen 1000  (Ethernet)
        RX packets 1927  bytes 147022 (143.5 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1729  bytes 118135 (115.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

## Apple-File-Protocol (AFP)

This will make the Pi an apple-file-protocol file-server that can be accessed in MacOS.

```
sudo apt-get install netatalk
```

Once netatalk is installed, the Raspberry will show up in the Mac Finder 'Shared' section. The Pi can be manually mounted from MacOS by going to `Go - Connect To Server...` and entering `afp://[piIP]` where [piIP] is the IP address of your Pi.

### Change the default name of your Pi in netatalk (optional)

When you mount the pi on MacOS, it will mount as `Home Directory` and the space in 'Home Directory' can cause problems. Change the name to something like 'pi3'.

See [this blog post][afpmountpoint] to change the name of the mount point from 'Home Directory'.    

In the following `the_name_you_want` should be changed to the name you want.

    # stop netatalk
    sudo /etc/init.d/netatalk stop

    # edit config file
    sudo pico /etc/netatalk/AppleVolumes.default

    # change this one line

    # By default all users have access to their home directories.
    #~/                     "Home Directory"
    ~/                      "the_name_you_want"

    # restart netatalk
    sudo /etc/init.d/netatalk start

When using the `pico` editor, `ctrl+x` to save and quit, `ctrl+w` to search, `ctrl+v` to page down. Remember, the `pico` editor does not respond to mouse clicks, you need to move the cursor around with arrow keys.

## Samba (SMB)

This will make the Pi a Samba (SMB) file server that can be accessed from both Windows and MacOS.

    sudo apt-get install samba samba-common-bin

Edit `/etc/samba/smb.conf`

	sudo pico /etc/samba/smb.conf

Add the following

	[share]
	Comment = Pi shared folder
	Path = /home/pi
	Browseable = yes
	Writeable = yes
	only guest = no
	create mask = 0777
	directory mask = 0777
	Public = yes
	Guest ok = no

Add a password

	sudo smbpasswd -a pi

Restart samba

	sudo /etc/init.d/samba restart
	
Test the server from another machine on the network. On a windows machine, mount the fileserver with `smb:\\[piIP]` where [piIP] is the IP address of your pi.

## Startup tweet

Have the Pi send a tweet with its IP when it boots. See [this blog post][startuptweeter] for instructions.
	
## Startup mailer

Have the Pi send an email with its IP address when it boots. See [this blog post][startupmailer] for instructions. An example python script is here, [startup_mailer.py][startupmailer]

## Have fun with your pi


[downloadraspian]: https://www.raspberrypi.org/downloads/
[installguide]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[mswindows]: http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/
[afpmountpoint]: http://blog.cudmore.io/post/2015/06/07/Changing-default-mount-in-Apple-File-Sharing/
[startupmailer]: https://github.com/cudmore/cudmore.github.io/blob/master/_site/downloads/startup_mailer.py
[startuptweeter]: http://blog.cudmore.io/post/2017/10/27/Raspberry-startup-tweet/
[uv4l]: http://blog.cudmore.io/post/2016/06/05/uv4l-on-Raspberry-Pi/
[putty]: http://www.putty.org/
[10]: https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address