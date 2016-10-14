---
layout: post
title: "Convert .h264 video with ffmpeg"
category: post
date: 2016-10-13 00:00:00
tags:
- video
---

This bash script will make new copies of all .h264 files in the current working directory

 - Output files will have 15 frames-per-second (-r 15)
 - Output files will be placed in /mp4/ directory
 - Output files will be renamed with .mp4 extension
 

    ~~~
    #INPUT="$1"
    
    mkdir mp4
    
    for file in *.h264 ; do
        filename="${file%.*}"
        echo $filename
        ffmpeg -r 15 -i "$file" -vcodec copy "mp4/$file.mp4"
        sleep 3
    done
    ~~~
