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

You want a name brand 'class 10' card with about 16 GB.

### 1.1) Download image

 [Download][downloadraspian] an image of the Raspian operating system. You want to 'Download ZIP' for 'Raspian Stretch Lite'.

 - As of Nov 16, 2017 the image was named `2017-09-07-raspbian-stretch-lite`.
 - As of April 19, 2018 the image was named `2018-04-18-raspbian-stretch-lite`.
 - As of Oct 17, 2018 the image was named `2018-10-09-raspbian-stretch-lite`.
 
### 1.2) Copy the downloaded image to SD card

If you run into trouble, follow this [installation guide][installguide]. 

#### On MacOS

Unzip the .zip file by right clicking the .zip file and selecting `Open With - Archive Utility.app (default)`. This will yield a .img file.

Insert an SD card into the Mac and use `DiskUtil` to format it as Fat32. You can find the `DiskUtility.app` in /Applications/utilities. In OSX Sierra this is DiskUtil - Erase - Format as 'MS-DOS (FAT)'.

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

Use DiskUtil to 'unmount' the SD card (don't eject, you need to unmount) or use this command line (assuming your sd card is /dev/disk4)

```
diskutil unmountDisk /dev/disk4
```

Copy the .img file to the SD card. Assuming your SD card was listed as /dev/disk4

```bash
sudo dd bs=1m if=/Users/cudmore/Downloads/2018-10-09-raspbian-stretch-lite.img of=/dev/rdisk4
```

Note that this command requires `/dev/rdisk` rather than `/dev/disk`. Once the .img is copying to the SD card, you will not get any feedback from the command line. You can either wait for it to finish (this can vary from 1-3 minutes) and if you are impatient, you can see the progress with keyboard ctrl+t.

Be very careful with this command, if you have multiple hard-drives make sure you specify the SD card we are using. If you get it wrong you could wipe an entire hard-drive.

Once dd is done, the SD card should re-appear on the desktop named 'boot'.

#### On Windows

Follow install guides [here][installguide].

### 1.3) Configure the Pi to run ssh at boot

The SSH server allows you to login to the Pi with a command prompt. Raspbian usually has the SSH server disabled by default and it needs to be activated manually. To do this, create an empty file named `ssh` in the root folder of the SD card.

On MacOS, open a terminal and type:

    touch /Volumes/boot/ssh
    
## 2) First boot of the Pi

The tricky part here is finding the Pi IP address. The easiest option is to use a home **router**.

 - Insert SD card into the Pi
 - Connect the Pi to a **router** with an ethernet cable
 - Plug in the USB power on the Pi.
 - Using another computer also plugged into the **router**, find the IP address of the Pi using the **router** web interface, usually http://192.168.1.1

### 2.1) Login via ssh

When you first login with ssh, you should see something like this and should answer yes with 'yes'.

```
The authenticity of host '192.168.1.6 (192.168.1.6)' can't be established.
ECDSA key fingerprint is SHA256:OGOP7N89ckn1krAxx1AwwqRhwmdBkJ2YIWl3GOlgQNw.
Are you sure you want to continue connecting (yes/no)?
```

#### On MacOS

In a terminal window, type the following, where `[piIP]` is address of your Pi you found in the previous step. The Terminal.app is in /Applications/Utilities in macOS.

    ssh pi@[piIP]
    #password is raspberry

#### On Windows

Download and use [Putty][putty].
    
### 2.2) Run configuration utility

On the command line, run the `raspi-config` utility with:

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

Here, we am setting my locale to 'en_US.UTF-8 UTF-8'. If you are in a different country you should set this as you want.

Once finished, reboot the system when asked or manually from the command line with `sudo reboot`.

### 2.3) Update the system

    sudo apt-get update --yes  #update database
    sudo apt-get upgrade --yes  #update userspace (this can take a long time)
    sudo reboot                #reboot

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

### Special instructions for The Johns Hopkins network

At Hopkins, using a computer already on the Hopkins network, point a browser to [https://jhars.nts.jhu.edu](https://jhars.nts.jhu.edu) and click 'Logon to JARS', enter your Hopkins login/password, and then “Register For a Fixed IP Address by Subnet”. Be careful as different ethernet wall jacks have different subnets. The subnet is the 3rd number in an IP address. For example 10.16.80.31 has subnet 80. If you do not know the subnet of where you are plugging into, plugin a spare laptop and figure out the subnet.

## Apple-File-Protocol (AFP)

This will make the Pi an apple-file-protocol file-server that can be accessed in MacOS.

```
sudo apt-get install netatalk --yes
```

Once netatalk is installed, the Raspberry will show up in the Mac Finder 'Shared' section. The Pi can be manually mounted from MacOS by going to `Go - Connect To Server...` and entering `afp://[piIP]` where [piIP] is the IP address of your Pi.

### Change the default name of your Pi in netatalk (optional)

When you mount the pi on MacOS, it will mount as `Home Directory` and the space in 'Home Directory' can cause problems. Change the name to something like 'pi3'.

See [this blog post][afpmountpoint] to change the name of the mount point from 'Home Directory'.    

In the following `the_name_you_want` should be changed to the name you want. One good strategy is to use the hostname.

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

    sudo apt-get install samba samba-common-bin --yes

Edit `/etc/samba/smb.conf`

	sudo pico /etc/samba/smb.conf

Copy and paste the following to the end of the file

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

	# this assumes the Pi has a /home/pi/video folder
	[video]
	Comment = Pi shared folder
	Path = /home/pi/video
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
	
Test the server from another machine on the network. On a windows machine, mount the fileserver with `smb:\\[piIP]` where [piIP] is the IP address of your pi. You should see two mount points, `share` and `video`.

## Mounting a USB drive

When you plugin a USB drive, it will not be automatically detected. This needs to be configured manually, please see [mounting a usb drive][mounting-a-usb-drive] for instructions.

## Startup email and tweet

It is useful to have the Pi send notifications when it boots. Please see the [startupnotify][startupnotify] Github repository.

<strike>Have the Pi send a tweet with its IP when it boots. See [this blog post][startuptweeter] for instructions.

Have the Pi send an email with its IP address when it boots. See [this blog post][startupmailer] for instructions. An example python script is here, [startup_mailer.py][startupmailer]
</strike>

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

## Have fun with your pi


[downloadraspian]: https://www.raspberrypi.org/downloads/raspbian/
[installguide]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[mswindows]: http://www.circuitbasics.com/raspberry-pi-basics-setup-without-monitor-keyboard-headless-mode/
[afpmountpoint]: http://blog.cudmore.io/post/2015/06/07/Changing-default-mount-in-Apple-File-Sharing/
[startupmailer]: https://github.com/cudmore/cudmore.github.io/blob/master/_site/downloads/startup_mailer.py
[startuptweeter]: http://blog.cudmore.io/post/2017/10/27/Raspberry-startup-tweet/
[uv4l]: http://blog.cudmore.io/post/2016/06/05/uv4l-on-Raspberry-Pi/
[putty]: http://www.putty.org/
[10]: https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address
[startupnotify]: https://github.com/cudmore/startupnotify
[mounting-a-usb-drive]: http://blog.cudmore.io/post/2015/05/05/mounting-a-usb-drive-at-boot/
