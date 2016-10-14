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

When you mount the pi on OSX, it will mount as 'Home Directory' and the space ' ' will cause problems. Change the name to something like 'pi3'.

See [this blog post][afpmountpoint] to change the name of the mount point from 'Home Directory'.    

### Change the default name of your Pi in netatalk

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

# Setup the network

### Configure /etc/network/interfaces

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

### Edit wpa_supplicant.conf

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

### Tell your router to assign an ip based on MAC address of wifi adapter

    ifconfig wlan0

The MAC address is listed as 'HWaddr' and in this case is '00:0b:81:89:11:8a'.

    wlan0     Link encap:Ethernet  HWaddr 00:0b:81:89:11:8a  
              inet addr:192.168.1.12  Bcast:192.168.1.255  Mask:255.255.255.0
              UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
              RX packets:1112 errors:0 dropped:837 overruns:0 frame:0
              TX packets:348 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:1000 
              RX bytes:253265 (247.3 KiB)  TX bytes:56154 (54.8 KiB)

# Make the Pi send email with IP on boot

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

    sudo crontab -e

Add this to end (sleep 5 does not work!!!!)

    @reboot (sleep 10; /home/pi/code/startup_mailer.py)

Now, when pi boots it will send an email with it's ip. Try it with

    sudo reboot

## Install screen

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

