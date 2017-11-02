---
layout: post
title: "libav for ffmpeg"
category: post
date: 2017-11-01 00:00:01
tags:
- linux
- raspberry
---

I have written this post countless times. Here I will finally switch to using libav over ffmpeg.

See my previous post on [ffmpeg][2]

See the [ffmpeg/libav][1] recipe I am following on the Debian wiki.

## Install
	sudo apt-get update
	sudo apt-get install libav-tools

avconv -r 15 -i ~/video/20171101/20171101_162658.h264 -r 15 -vcodec copy mp4/20171101_162658.mp4


[1]: https://wiki.debian.org/ffmpeg
[2]: Convert-h264-files-with-ffmpeg