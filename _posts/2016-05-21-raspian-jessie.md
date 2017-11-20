---
layout: post
title: "Installing Raspian Jessie on a Raspberry 2/3"
category: post
date: 2016-05-21 01:01:06
tags:
- raspberry
- linux
---

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

Insert SD card and format as Fat32 with DiskUtil.

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
sudo dd bs=1m if=/Users/cudmore/Downloads/2017-09-07-raspbian-stretch-lite.img of=/dev/rdisk3
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
   
Selecting Boot Options -> Console is important. It seems Raspbian ships with X-Windows on by default and you want to turn it off.

### 2.3) Update the system

    sudo apt-get update  #update database
    sudo apt-get upgrade #update userspace
    sudo rpi-update      #update firmware (requires reboot)
    sudo reboot          #reboot

## Setup the network

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

This will make the Pi a file-server that can be accessed from a MacOS computer with apple-file-protocol (afp).

    sudo apt-get install netatalk

Once netatalk is installed, the Raspberry will show up in the Mac Finder 'Shared' section


#### Change the default name of your Pi in netatalk

When you mount the pi on MacOS, it will mount as 'Home Directory' and the space ' ' will cause problems. Change the name to something like 'pi3'.

See [this blog post][afpmountpoint] to change the name of the mount point from 'Home Directory'.    

    # stop netatalk
    sudo /etc/init.d/netatalk stop

    # edit config file
    sudo nano /etc/netatalk/AppleVolumes.default

    # change this one line

    # By default all users have access to their home directories.
    #~/                     "Home Directory"
    ~/                      "pi50"

    # restart netatalk
    sudo /etc/init.d/netatalk start

## Make the Pi send email with IP on boot (20171120, no longer works)

Create an executable python script to send en email with IP. An example [startup_mailer.py][startupmailer]

    mkdir code
    cd code
    wget https://github.com/cudmore/cudmore.github.io/raw/master/_site/downloads/startup_mailer.py
    chmod +x startup_mailer.py

Make sure the first line in the .py code is `#!/usr/bin/python`.

    #!/usr/bin/python

Set the email parameters in startup_mail.py

	to = 'robert.cudmore@gmail.com'
	gmail_user = 'cudmore.raspberry@gmail.com'
	gmail_password = 'ENTER_YOUR_PASSWORD_HERE'

Run crontab as root and append one line `@reboot (sleep 10; /home/pi/code/startup_mailer.py)`

    crontab -e

Add this to end (sleep 5 does not work!!!!)

    @reboot (sleep 10; /home/pi/code/startup_mailer.py)

Now, when pi boots it will send an email with it's ip. Try it with

    sudo reboot

## Install uv4l (optional for video streaming)

See [uv4l-on-Raspberry-Pi][uv4l]

## Install screen (optional)

    sudo apt-get install screen

Any code run inside a screen session will continue to run even after ou logout of the system.

    screen #start a screen session
    python my_python_code.py #start some code
    #detatch from screen with ctrl+a then d
    #logout
    #log back in
    screen -r #resume your screen session and you will see your code is still running
    #don't forget to detatch again with ctrl+a then d

   
[downloadraspian]: https://www.raspberrypi.org/downloads/
[installguide]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[mswindows]: http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/
[afpmountpoint]: http://blog.cudmore.io/post/2015/06/07/Changing-default-mount-in-Apple-File-Sharing/
[startupmailer]: https://github.com/cudmore/cudmore.github.io/blob/master/_site/downloads/startup_mailer.py
[uv4l]: http://blog.cudmore.io/post/2015/06/05/uv4l-on-Raspberry-Pi/
[putty]: http://www.putty.org/
