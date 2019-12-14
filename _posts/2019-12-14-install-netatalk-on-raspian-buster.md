---
layout: post
title: "Installing Netatalk (afp) on Raspian Buster"
category: post
date: 2019-12-14 01:02:06
---

This is a recipe to install NetATalk (AFP) on a Raspberry Pi with Raspian Buster.

### Netatalk, aka apple-file-protocol (AFP)

Thanks to the following for the solution: [https://www.raspberrypi.org/forums/viewtopic.php?t=243785][https://www.raspberrypi.org/forums/viewtopic.php?t=243785]

The  configuration script is now in `/etc/netatalk/afp.conf`.

Assuming each of your Pi's have a unique `host name`, you can set the mount point of AFP with the following. The mount point is the name of the volume that appears on your desktop when you use network connect afp://[ip] and is available in /Volumes

Stop netatalk

```
sudo /etc/init.d/netatalk stop
```

Edit `/etc/netatalk/afp.conf`

```
sudo pico /etc/netatalk/afp.conf
```

Append the following

```
[$h]
    path = /home
    home name = $h
```

Restart netatalk

```
sudo /etc/init.d/netatalk stop
```

Now, on macOS, if you mount with 'Go - Connect TO Server' and enter `afp://[IP]` whre `[IP]` is the IP address of your Buster Pi, the Pi will mount on your desktop as `hostname` where hostname is the name you specify in `sudo raspi-config`.
