---
layout: post
title: "Prairie scope analysis"
category: post
date: 2016-11-20 00:00:00
tags:
- analysis
---

Acquisition and analysis workflow for Prairie two-photon scope

PUT THIS TOGETHER WITH CURRENT NOTES SITTING ON DESKTOP OF SCOPE COMPUTER

[Operator's Manual][Ultima-Operators-Manual-Rev-B] pdf

Scope ID is 4647

[Original Quote][1] pdf

[Download Prairie View][3]. Password for 5.3 is 'glial'

## Current workflow

 - prairie2tif_.py : Convert single image .tif directories (saved by Prairie) into single .tif stacks
 - bAlignFolder_.py : Align on channel 2 (GFP) and apply alignment to channel 1
 - bAvgTimeSeries_.py : Average n_avg number of frames to make new stack where output stack has n_orig/n_avg number of frames. Keep an eye on dwell time and samples average per pixel.
 
## To Do (understanding how to acquire good images)

  - There is a lot of shot noise in my images. Either laser is too high or PMT gain is too high. This shot noise has similar intensity to my GFP signal, this is bad.
  
## To Do (Pre-process raw data)
 
  - write bAvgTimeSeries_.py
  - I need some median filter somehwere. Decide if I do this before or after frame averaging? My guess is before? Add median filter (3 pixels) to bAvgTimeSeries_.py
  
  - Write a 'meta' batch to (i) prairie2tif_ (ii) bAlignFolder_ (iii) bAvgTimeSeries_

  - Modify prairie2tif_.py to optionally spit out a comma delimited report, one stack per row, with all detection parameters.
 
## To Do (Efficiency)

  - Figure out how to have multiple instances of Fiji running so we can speed up alignment with MultiStackReg in bAlignFolder_.py. Right now if I run this alignment on 10 stacks with 1800 frames and two channels it takes 96 minutes (5738.76 seconds).
    
## To Do (Video)

  - Write bash script to convert all video in a session from .h264 to .mp4. Put output into /mp4/ folder.
  - Figure out the correspondence between my acquired Prairie time-series and my video. Video is labelled with frame numbers but Prairie outputs more frames (via end of frame ttl) than are actually acquired..
  
## To Do (Igor)

  - Bring it all together in Igor
  - Load a generic directory of AvgTimeSeries
  - Load a directory of Raspberry .txt files (not neccessary?)
  - Load a directory of .mp4 videos
  - Synch AvgTimeSeries stack with video
  - Use LineTool to draw (and save) lines across vessels and get diameter through time
  - Use stack/video synching to verify movement evokes capillary dilation/constriction
  
## To Do (the fucking analysis)

  - Use this hole system to first look at surface arteries and veins
  - Then look at 1st or branches of diving arteries/veins. Arteries don't really branch? Determine if 1st order off ascending veins dilate/constrict in response to movement.
  
## Ideas

  - Try and estimate blood flow by integrating/averaging fluorescence in a tube across time. There are always green specs flying by, if flow goes up there should be more specs and it should be on average brighter.
  
## Converting .h264 to .mp4

 - Double check triggercamera.py to verify 30 fps
 - Run this script from within folder with .h264 files
 
```bash
#!/bin/bash

#INPUT="$1"

mkdir mp4

for file in *.h264 ; do
	filename="${file%.*}"
	echo $filename
	ffmpeg -r 30 -i "$file" -vcodec copy "mp4/$file.mp4"
	sleep 3
done
```

## Raspberry

Raspberry ip is 10.16.81.61

## Raspberry To Do

  - Have igor signal animal ID to REST interface
  - When Igor is master, signal file that will be saved to rest interface. We need to use file number, not name as we don't know if Prairie software will be acquiring z-stack, time-series, line scan, etc (they have different names)
  - Have PiCamera save current frame when it received a frame TTL. PiCamera has at least two different 'current frame' variables, figure out which one
  - Make sure I get PiCamera fps somewhere in saved _r.txt file. Igor is having trouble finding this.
  
## Prairie View blog with updates and release notes

https://pvupdate.blogspot.com/

## Fiji plugin for prairie

See Prairie View blog side-bar

https://www.dropbox.com/s/in593hvhc2v3dwj/Prairie_Reader.zip?dl=0

## Prairie emission filters

Scope ID is 4647, use to search email for long threads with technicians ending around 11/11/16 - 12/5/16

This is from the original [scope quote][1] (20150528), assuming it is what we have?

Dual emission filters (et525/70m-2p and et595/50m-2p) and t565lpxr dichroic beam splitter for simultaneous viewing and acquisition from both detectors

 - green band pass filter (could not find 70m version) is (et525/50m-2p)[https://www.chroma.com/products/parts/et525-50m]
 - red band-pass filter is (et595/50m-2p)[https://www.chroma.com/products/parts/et595-50m]
 - dichroic beam splitter is (t565lpxr)[https://www.chroma.com/products/parts/t565lpxr]

See Thermo Fischer Fluorescence SpectraViewer for (Texas Red emission profile)[https://www.thermofisher.com/us/en/home/life-science/cell-analysis/labeling-chemistry/fluorescence-spectraviewer.html]

With red filter centered at 595 nm we are collecting ~ 50% of Texas Red emission. But the band is 50m which should do the job? But may not be enough?

## Sutter red filter

This is from email to Zeng You 20150416, did he replace this?

The red filter in front of the PMT is from Chroma and is a HQ 610/75m

(HQ 610/75m)[https://www.chroma.com/products/parts/hq610-75m]


## Synch code to robertcudmore.org

Treadmill is synching code to robertcudmore.org with unison

Install unison with

    sudo apt-get install unison
    
Save this into `/home/pi/.unison/treadmill.prf`

```bash
# Unison preferences file
root = /home/pi/Sites/treadmill
root = ssh://robertcu@robertcudmore.org/raspberry/Sites/treadmill

#ignore = Path */raw/*

ignore = Name *.pyc
ignore = Name .git*
ignore = Name .*
ignore = Name .DS_Store
ignore = Name *.DS_Store
ignore = Name *.shtml
ignore = Name *.htaccess

# Be fast even on Windows
#fastcheck = yes

servercmd=/home1/robertcu/unison
```

[1]: /images/JHU-15-051120E.pdf
[Ultima-Operators-Manual-Rev-B]: /images/Ultima-Operators-Manual-Rev-B.pdf
[3]: https://pvupdate.blogspot.com/