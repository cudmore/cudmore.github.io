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

This was originally written for Jessie in May 2016 and then updated for Stretch on Nov 22, 2017.

## 1) Set up the SD card

With the SD card inserted into a card-reader on an existing computer.

### 1.1) Download image

 - As of May 21, 2016 the image was named `2016-05-10-raspbian-jessie`.
 - As of Nov 16, 2017 the image was named `2017-09-07-raspbian-stretch-lite`.
 [Download here][downloadraspian]

### 1.2) Copy the downloaded image to SD card

For either MacOS or Windows, follow an installation guide [here][installguide]. 

#### On MacOS

Unzip the .zip file by right clicking the .zip file and selecting 'Open With - Archive Utility.app (default)'. This will yield a .img file.

Insert SD card and use DiskUtil to format it as Fat32.

Use DiskUtil to 'unmount' the SD card (don't eject, you need to unmount)

Find the location of your SD card, in a terminal type `diskutil list`.

You should see something like this.

```
/dev/disk9
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *15.9 GB    disk9
   1:             Windows_FAT_32 boot                    43.8 MB    disk9s1
   2:                      Linux                         1.8 GB     disk9s2
```

Copy the .img file to the SD card. Assuming your SD card was listed as /dev/disk9

```bash
sudo dd bs=1m if=/Users/cudmore/Downloads/2017-09-07-raspbian-stretch-lite.img of=/dev/rdisk9
```

#### On Windows

Follow install guides [here][installguide].

### 1.3) Configure the Pi run ssh on boot

As of the November 2016 release, Raspbian has the SSH server disabled by default. You will have to enable it manually. To enable the ssh server, create a file named 'ssh' in the root folder of the SD card

On MacOS, open a terminal and type:

    touch /Volumes/boot/ssh
    
## 2) First boot of the Pi

Insert SD card into a Pi, connect Pi to a router with an ethernet cable and boot

Find IP address using router web interface, usually http://192.168.1.1

### 2.1) Login via ssh

#### On MacOS

In a terminal window, type the following, where IP address is address of your Pi you found in the previous step.

    ssh pi@192.168.1.15
    #password is raspberry

#### On Windows

You are on your own, download and use [Putty][putty].
    
### 2.2) Run configuration utility

    sudo raspi-config

20171122 - The name and location of these options have changed. This is still the general idea

 - 1 Change User password
 - 2 Hostname -> [Chose a name]
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
     
Selecting Boot Options -> Console is important. It seems Raspbian ships with X-Windows on by default and you want to turn it off.

### 2.3) Update the system

    sudo apt-get update  #update database
    sudo apt-get upgrade #update userspace (this can take a long time)
    sudo rpi-update      #update firmware (requires reboot)
    sudo reboot          #reboot

## Setup the network

If you are connecting to a router there is no additional setup required.

20171122, With Raspbian Stretch this got complicated again. See [this][10]

When on a university network (At least the Hopkins network), it is strongly suggested to use hard wiring with an ethernet cable rather than relying on wifi.

#### Configure /etc/network/interfaces

The stock install of Raspian should already have this.

```
sudo pico /etc/network/interfaces
```

    auto lo

    iface lo inet loopback
    iface eth0 inet dhcp

    allow-hotplug wlan0
    iface wlan0 inet manual
    wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
    iface default inet dhcp

20171122 Raspbian Stretch the file now contains

```
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d
```

#### Edit wpa_supplicant.conf

At Hopkins you want to follow [these instruction](http://www.it.johnshopkins.edu/services/network/wireless/wpasupplicant.html)

```
sudo pico /etc/wpa_supplicant/wpa_supplicant.conf 
```

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="NETGEAR28"
        psk="your_password_here"
    }

    # "hopkins" wireless for JHU
    network={
        ssid="hopkins"
        key_mgmt=WPA-EAP
        eap=PEAP
        phase2="auth=MSCHAPV2"
        identity="JHED_ID_Replace_Me"
        password="JHED_Password_Replace_Me"
    }

#### Tell your router to assign an ip based on MAC address of wifi adapter

    ifconfig wlan0

The MAC address is listed as 'HWaddr' and in this case is '00:0b:81:89:11:8a'.

    wlan0     Link encap:Ethernet  HWaddr 00:0b:81:89:11:8a  
              inet addr:192.168.1.12  Bcast:192.168.1.255  Mask:255.255.255.0
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:1112 errors:0 dropped:837 overruns:0 frame:0
              TX packets:348 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000 
              RX bytes:253265 (247.3 KiB)  TX bytes:56154 (54.8 KiB)


## AFP / Netatalk / Avahi

This will make the Pi an apple-file-protocol file-server that can be accessed MacOS.

    sudo apt-get install netatalk

Once netatalk is installed, the Raspberry will show up in the Mac Finder 'Shared' section. The Pi can be manually mounted from MacOS by going to `Go - Connect To Server...` and entering `afp://IP` where IP is the IP address of your Pi.

#### Change the default name of your Pi in netatalk

When you mount the pi on MacOS, it will mount as 'Home Directory' and the space ' ' will cause problems. Change the name to something like 'pi3'.

See [this blog post][afpmountpoint] to change the name of the mount point from 'Home Directory'.    

In the following `the_name_you_want` should be changed to the name you want.

    # stop netatalk
    sudo /etc/init.d/netatalk stop

    # edit config file
    sudo nano /etc/netatalk/AppleVolumes.default

    # change this one line

    # By default all users have access to their home directories.
    #~/                     "Home Directory"
    ~/                      "the_name_you_want"

    # restart netatalk
    sudo /etc/init.d/netatalk start


## Samba

This will make the Pi a Samba (SMB) file server that can be accessed from both Windows and MacOS.

    sudo apt-get install samba samba-common-bin

Edit `/etc/samba/smb.conf`

	sudo pico /etc/samba/smb.conf

Add the following

	[share]
	Comment = Pi shared folder
	Path = /home/pi
	Browseable = yes
	Writeable = Yes
	only guest = no
	create mask = 0777
	directory mask = 0777
	Public = yes
	Guest ok = no

Add a password

	sudo smbpasswd -a pi

Restart samba

	sudo /etc/init.d/samba restart
	
Test the server from another machine on the network. On a windows machine, mount the fileserver with `smb:\\IP` where IP is the IP address of your pi.

## Install additional python packages (optional)

    # assuming you want python 2.7
    sudo apt-get install python-pip
    
    # pi camera
    sudo apt-get install python-picamera

    
## Startup tweet

Have the Pi send a tweet with its IP when it boots. See [this blog post][startuptweeter] for instructions.
	
## Startup mailer

Have the Pi send an email with its IP address when it boots. See [this blog post][startupmailer] for instructions. An example python script is here, [startup_mailer.py][startupmailer]

## Install uv4l (optional for video streaming)

See [uv4l-on-Raspberry-Pi][uv4l] for instructions.

## Install unison (optional)

If you don't know what unison is then don't install it.

My remote server (via bluehost) has unison 2.4 installed. The newest version of Raspbian Jessie is using unison 2.8. I need to roll back unison on Raspberry to 2.4 for this to work


    mkdir tmp
    cd tmp
    wget http://mirrordirector.raspbian.org/raspbian/pool/main/u/unison/unison_2.40.65-2_armhf.deb
    sudo dpkg -i unison_2.40.65-2_armhf.deb 

```
sudo apt-get install unison
# see link to set up auto authentication with rsa keys
unison # run once to make /home/pi/.unison
pico /home/pi/.unison/sites.prf    

# This is contents of /home/pi/.unison/sites.prf
# Unison preferences file
root = /home/pi/Sites
root = ssh://robertcu@robertcudmore.org/raspberry/Sites

ignore = Name *.tif
ignore = Name .AppleDouble
ignore = Name .DS_Store
ignore = Name *.DS_Store
ignore = Name *.shtml
ignore = Name *.htaccess

# Be fast even on Windows
# fastcheck = yes

servercmd=/home1/robertcu/unison
```


   
[downloadraspian]: https://www.raspberrypi.org/downloads/
[installguide]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[mswindows]: http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/
[afpmountpoint]: http://blog.cudmore.io/post/2015/06/07/Changing-default-mount-in-Apple-File-Sharing/
[startupmailer]: https://github.com/cudmore/cudmore.github.io/blob/master/_site/downloads/startup_mailer.py
[startuptweeter]: http://blog.cudmore.io/post/2017/10/27/Raspberry-startup-tweet/
[uv4l]: http://blog.cudmore.io/post/2015/06/05/uv4l-on-Raspberry-Pi/
[putty]: http://www.putty.org/
[10]: https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address