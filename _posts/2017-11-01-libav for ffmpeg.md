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

## convert

The .h264 is primarily designed for streaming and does not have the concept of fps (it is determined by the rate of streaming).

Here we convert `20171108_102418.h264` into `20171108_102418.mp4` with 15 fps.

    avconv -i 20171108_102418.h264 -r 15 -vcodec copy mp4/20171108_102418.mp4

## to do

Write bash script to convert a directory of .h264 into .mp4 (with fps)


[1]: https://wiki.debian.org/ffmpeg
[2]: Convert-h264-files-with-ffmpeg