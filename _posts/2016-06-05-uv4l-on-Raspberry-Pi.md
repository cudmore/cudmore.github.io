---
layout: post
title: "uv4l on Raspberry Pi"
category: post
date: 2016-06-05 01:01:06
tags:
- raspberry
- debian
- linux
- video
---

The uv4l people have update their code and you can now stream real-time high resolution video to a browser. And it works on the Raspberry Pi.

Install drivers

    http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=14

Run driver

    uv4l --driver raspicam --auto-video_nr --width 640 --height 480 --encoding jpeg
    
Kill

    pkill uv4l
    
Extensize list of use cases

    http://www.linux-projects.org/modules/sections/index.php?op=viewarticle&artid=16#example11
    
    