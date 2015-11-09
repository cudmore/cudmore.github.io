---
layout: post
title: "debian server"
category: post
date: 2015-11-07 22:01:06
tags:
- osx
- linux
---

Goal is to set up a home server running Debain Jessie.

##0) The hardware is as follows
  - See my pcpartspicker [inventory](http://pcpartpicker.com/p/PRq8Vn)
  - Processor: Intel Pentium G3258 3.2GHz Dual-Core Processor
  - Motherboard: Gigabyte GA-H97N-WIFI Mini ITX LGA1150 Motherboard
  - RAM: G.Skill Sniper Series 8GB (2 x 4GB) DDR3-1866 Memory
  - Case: Cooler Master Elite 110 Mini ITX Tower Case
  - Power: EVGA 430W 80+ Certified ATX
  
##1) Download and install debian

  - Download debian jessie
  - Make a usb key
  - Install debian
  - Check your debian version
  ```
  cat /etc/debian_version 
  8.2
  ```

##2) Configure debian jessie

###Update your repositories

  ```
  apt-get update
  ```

###ssh

  ```
  apt-get install openssh-server
  ```
  
  - Follow [this](https://wiki.debian.org/SSH#Installation_of_the_server)
    
###Sudo
  - Use apt-get to install sudo. This is better then switching to su.
  - Follow [this](https://wiki.debian.org/sudo).

###Add in a second hard drive
  - partition
  
  ```
  cfdisk /dev/sdb
  ```

  - format

  ```
  mkfs.ext4 /dev/sdb1
  ```

  - Once disk is partitioned and formatted, this is what it looks like
  
  ```
  cudmore@debian:~$ sudo fdisk -l /dev/sdb
  Disk /dev/sdb: 1.8 TiB, 2000398934016 bytes, 3907029168 sectors
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes
  Disklabel type: gpt
  Disk identifier: 8B1D619B-4B38-44AE-AEE1-0180F07FC75F
  
  Device     Start        End    Sectors  Size Type
  /dev/sdb1   2048 3907029134 3907027087  1.8T Linux filesystem
  ```

  - Mount the second harddrive in a folder /movies

  ```
  mkdir /movies # remember to set group and group rwx later
  mount -t ext4 /dev/sdb1 /movies
  ```

  - blkid to get unique name for fstab entry
  
  ```
  cudmore@debian:~$ sudo blkid
  /dev/sda1: UUID="30EE-7B6B" TYPE="vfat" PARTUUID="1eae1e11-6902-45f9-9c27-55ab648972b3"
  /dev/sda2: UUID="2cf97347-1baf-4abf-a297-650ebf4dfdff" TYPE="ext4" PARTUUID="15ac40fa-5874-423b-9282-209a8b88a60a"
  /dev/sda3: UUID="16a7a205-220c-4583-a758-4fcaf3eb0417" TYPE="swap" PARTUUID="fa435c81-ab1e-4192-97ba-e55c08ceb932"
  /dev/sdb1: UUID="f6b5096b-188b-4204-92aa-31e8c58e0eb6" TYPE="ext4" PARTUUID="61e5434f-7975-45a8-a8c4-6148fb56f9b4"
  ```

  - Append the new disk to /etc/fstab

  ```
  cudmore@debian:~$ more /etc/fstab 
  # /etc/fstab: static file system information.
  #
  # Use 'blkid' to print the universally unique identifier for a
  # device; this may be used with UUID= as a more robust way to name devices
  # that works even if disks are added and removed. See fstab(5).
  #
  # <file system> <mount point>   <type>  <options>       <dump>  <pass>
  # / was on /dev/sda2 during installation
  UUID=2cf97347-1baf-4abf-a297-650ebf4dfdff /               ext4    errors=remount-ro 0       1
  # /boot/efi was on /dev/sda1 during installation
  UUID=30EE-7B6B  /boot/efi       vfat    umask=0077      0       1
  # swap was on /dev/sda3 during installation
  UUID=16a7a205-220c-4583-a758-4fcaf3eb0417 none            swap    sw              0       0
  # 2tb drive for movies
  UUID=f6b5096b-188b-4204-92aa-31e8c58e0eb6 /movies ext4 errors=remount-ro 0 1
  ```
  
###Users and groups

  - Make a second user 'user2'

  ```
  sudo adduser user2
  ```

  - Make a group 'movies'

  ```
  sudo addgroup movies
  ```
  - Add myself (user1) and user2 to the 'movies' group

  ```
  sudo usermod -a -G movies user1
  sudo usermod -a -G movies user2
  ```

###Make second harddrive rwx for group 'movies'
  - make sure the second hard drive has rwx permission for group 'movies'

  ```
  #the first 'movies' is the name of the group, the second /movies is the folder
  sudo chgrp -R movies /movies
  sudo chmod -R g+rwx /movies
  ```

###afp

  - Follow [debian jessie afp install guide](http://netatalk.sourceforge.net/wiki/index.php/Install_Netatalk_3.1.7_on_Debian_8_Jessie)
 
  - I am using netatalk-3.1.7
  - Modify /usr/local/etc/afp.conf

  The key here is to specify the name of the mount point using 'home name = $u_server'. Otherwise your mount point becomes '[[user]]'s home' and programs like Microsoft Word and Fiji will probably not find the path with the apostrophe in the name.

$u is a variable that inserts the current username. It is defined in the [afp.conf](http://netatalk.sourceforge.net/3.0/htmldocs/afp.conf.5.html) documentation.

[movie_server] is a mount point that will mount my second hard drive from folder /movies.

  ```
  ;
  ; Netatalk 3.x configuration file
  ;
  
  [Global]
  ; Global server settings
  
  [Homes]
  ; basedir regex = /xxxx
    ;user1 will mount as user1_server
    home name = $u_server
    basedir regex = /home
  
  ; [My AFP Volume]
  ; path = /path/to/volume
  
  [movies_server]
  path = /movies
  ```

###Remote desktop with vnc
  - This is not working. May be jessie bug?
  - [plagiarized guide](http://linuxconfig.org/quick-vnc-server-client-setup-on-debian-linux-jessie-8)
  
###Install Anaconda
  - Download and follow [these](http://docs.continuum.io/anaconda/install#linux-install) instructions on website
  
###Configure [duckdns](https://www.duckdns.org) to keep your external/router ip up to date
  - Follow [this](https://www.duckdns.org/install.jsp)

###Install samba/smb
  - Follow something like [this](https://wiki.debian.org/SambaServerSimple)
  - edit with 'sudo pico /etc/samba/smb.conf'

  ```
  [movies_server]
   comment = movies on debian server
   read only = no
   locking = no
   path = /path_to_our_files
   guest ok = no
   ```

   - Restart samba
   ```
   sudo /etc/init.d/samba restart
   ```
   
###Get a python script to runat boot
  - This is very unclear to me
  - Directly edit 'sudo pico /etc/crontab'
  
  ```
  @reboot root /home/cudmore/anaconda2/bin/python /home/cudmore/Sites/temperatureserver/app.py >> /home/cudmore/Sites/temperatureserver/temperatureserver.log 2>&1
  ```
  
  - I want this to redirect stdout to the .log file. It is redirecting when it starts up but is not redirecting my 'print' statements as it runs?
  
###Install transmission

  - sudo apt-get install transmission
  - sudo apt-get install transmission-daemon
  - - Follow very specific instructions [here](https://trac.transmissionbt.com/wiki/HeadlessUsage/General)
  
