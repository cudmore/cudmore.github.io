---
layout: post
title: "Convert .h264 video with ffmpeg"
category: post
date: 2016-10-25 00:00:00
tags:
- linux
---

Mount a remote folder 10.16.80.212/share into a folder /mnt/datashare. Use /etc/fstab so this remote folder is mounted on every boot.

- Edit fstab

    sudo pico /etc/fstab

- Add a line like this

    //10.16.80.212/share    /mnt/datashare  cifs    user=cudmore,pass=mypassword,uid=pi,gid=pi        0       0

Here, we mount a remote folder (//10.16.80.212/share) into a local directory (/etc/datashare). The remote machine is logged in via a user (cudmore) with password (mypassword). Once mounted, the local folder (/mnt/datashare) will have user/owner (pi) and group (pi).


- Mount by hand

    sudo mount -a
    
- Unmount

    sudo umount /mnt/datashare

	# if /mnt/datashare is not mounted, you will get
	# umount: /mnt/datashare/: not mounted
	

    
