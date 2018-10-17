---
layout: post
title: "Mounting a USB drive at boot"
category: post
date: 2015-05-05 22:01:06
tags:
- linux
- raspberry
---

I have a Fat32 formatted USB drive and I want to have it mounted when the Raspberry Pi boots. To do this I add an entry to my fstab file using the UUID of the drive and some permission.

#### Get a list of your USB devices to check if your USB drive is available

    lsusb

	Bus 001 Device 002: ID 0424:9514 Standard Microsystems Corp.
	Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
	Bus 001 Device 003: ID 0424:ec00 Standard Microsystems Corp.
	Bus 001 Device 004: ID 13fe:5200 Kingston Technology Company Inc.
	Bus 001 Device 005: ID 0bda:8176 Realtek Semiconductor Corp. RTL8188CUS 802.11n WLAN Adapter

#### Make a directory to mount your drive/volume into

    sudo mkdir /home/pi/video

#### Find the UUID of your drive

	sudo blkid

	/dev/mmcblk0p1: SEC_TYPE="msdos" LABEL="boot" UUID="2654-BFC0" TYPE="vfat"
	/dev/mmcblk0p2: UUID="548da502-ebde-45c0-9ab2-de5e2431ee0b" TYPE="ext4"
	/dev/sda1: LABEL="video" UUID="7CCD-19F2" TYPE="vfat"

This tells me that my usb drive is in the device list at /dev/sda1, has the label ‘video’, a UUID of ’7CCD-19F2′, and is formatted as VFAT (e.g. FAT32).

#### Edit your /etc/fstab file by appending a line for your dive

	sudo pico /etc/fstab

	proc            /proc           proc    defaults          0       0
	/dev/mmcblk0p1  /boot           vfat    defaults          0       2
	/dev/mmcblk0p2  /               ext4    defaults,noatime  0       1
	UUID=7CCD-19F2 /home/pi/video    vfat    rw,umask=0      0       0
	# a swapfile is not a swap partition, so no using swapon|off from here on, use $

Here, on the line starting with UUID, I have mounted a device using its UUID=7CCD-19F2 into a folder /home/pi/video. This is a Fat32 formatted drive (vfat) and everybody has read-write permissions (rw,umask=0). This recipe will not work for other types of formatted drives (Ext3, NTFS, etc).

#### Remount Your drives and check the drive is mounted

	sudo mount -a

'ls' should show /video/ in blue to indicate it is mounted

Important. When you make the directory where a drive will be mounted it MUST be done with ‘sudo mkdir /home/pi/video’. You need ‘sudo’ so fstab can mount it on boot, the final permissions of this mounted drive are set in the drives fstab line. In this case, ‘rw,umask=0′.

#### Linux Commands

- List your usb devices: lsusb

- List the Location, Label, UUID and Type of your USB devices: sudo blkid

- Unmount a volume: sudo umount /home/pi/video

- Mount everybody in fstab: sudo mount -a

- Check if a drive is mounted: df | grep “/home/pi/video” | awk ‘{print $6}’

#### To Do

- A problem I just had is that my USB drive did not get mounted at boot and the folder I have reserved for it is on my root file system, ‘/’,  with only 4 GB of space. I started writing tons of video files to the folder and quickly ran out of space on. Now, I need a way to test if the folder I am writing to is (I) a folder or (ii) an actual mount point. Tym, the bash guru in the lab and my go to person on these things suggested the following:

	df | grep “/home/pi/video” | awk ‘{print $6}’

This will return an empty string if /home/pi/video is NOT mounted.

