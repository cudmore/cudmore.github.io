---
layout: post
title: "Installing uv4l on Raspian Buster"
category: post
date: 2019-12-14 01:01:06
---

This is a recipe to install uv4l on a Raspberry 4 computer with Raspian Buster. Not much has changed since Raspian Stretch. As this recipe is followed, please pay attention to the details!

After this install, run `uv4l` as follows:

```
uv4l --driver raspicam --auto-video_nr --encoding h264 --enable-server on
```

And then view the stream in a browser with (pleae note your IP address might be different)

```
http://192.168.1.9:8080/stream
```

Please see my video controller software [PiE](http://blog.cudmore.io/pie-doc/), it uses uv4l out of the box on both Stretch and Buster.

### Recipe

(1)

Add the uv4l key to your apt-key package manager.

```
curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc | sudo apt-key add -
```

**Note:** I am not sure what the difference is between `lpkey.asc` and `lrkey.asc`? My installations on Stretch were using the wrong key! I was using `lrkey.asc` while I should have been using the `p` variant `lpkey.asc`. Not sure why this worked on Stretch but it did. For Buster, you **must** use `lpkey.asc`.

(2) Add the following line to `/etc/apt/sources.list` using `sudo pico /etc/apt/sources.list`

```
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main
```

(3) Update apt-get and install with apt-get using

```
sudo apt-get update
sudo apt-get install uv4l uv4l-server uv4l-raspicam
```

**Important:** I was previously using `sudo apt-get -qq --allow-unauthenticated install uv4l uv4l-server uv4l-raspicam` and with Buster, the use of `--allow-unauthenticated` seems to break the install?

(4) Run the uv4l server with

```
uv4l --driver raspicam --auto-video_nr --encoding h264 --width 1280 --height 720 --enable-server on
```

And then view the stream in a browser with (please note your IP address might be different)

```
http://192.168.1.9:8080/stream
```

### Troubleshooting

Sometimes you get multiple `/dev/video0`, `/dev/video1`, `/dev/video10` excetera devices. Feel free to remove them with `sudo rm /dev/video*` and then maybe restart with `sudo reboot`.

### Details:

`sudo apt-get update` returns

```
Hit:1 http://archive.raspberrypi.org/debian buster InRelease
Hit:2 http://raspbian.raspberrypi.org/raspbian buster InRelease                
Hit:3 http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch InRelease
Reading package lists... Done
```

`sudo apt-get install uv4l uv4l-server uv4l-raspicam` returns

```
Reading package lists... Done
Building dependency tree       
Reading state information... Done
uv4l is already the newest version (1.9.17).
uv4l-raspicam is already the newest version (1.9.63).
The following additional packages will be installed:
  libssl1.0.2
The following NEW packages will be installed:
  libssl1.0.2 uv4l-server
0 upgraded, 2 newly installed, 0 to remove and 1 not upgraded.
Need to get 2,582 kB of archives.
After this operation, 8,237 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch/main armhf uv4l-server armhf 1.1.125 [1,689 kB]
Get:2 http://mirrors.ocf.berkeley.edu/raspbian/raspbian buster/main armhf libssl1.0.2 armhf 1.0.2q-2 [893 kB]
Fetched 2,582 kB in 5s (511 kB/s)                                       
Preconfiguring packages ...
Selecting previously unselected package libssl1.0.2:armhf.
(Reading database ... 45170 files and directories currently installed.)
Preparing to unpack .../libssl1.0.2_1.0.2q-2_armhf.deb ...
Unpacking libssl1.0.2:armhf (1.0.2q-2) ...
Selecting previously unselected package uv4l-server.
Preparing to unpack .../uv4l-server_1.1.125_armhf.deb ...
Unpacking uv4l-server (1.1.125) ...
Setting up libssl1.0.2:armhf (1.0.2q-2) ...
Setting up uv4l-server (1.1.125) ...
Processing triggers for libc-bin (2.28-10+rpi1) ...
Processing triggers for man-db (2.8.5-2) ...
```


This is the contents of `/etc/apt/source.list`

```
deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
# Uncomment line below then 'apt-get update' to enable 'apt-get source'
#deb-src http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi
deb http://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main
```

