---
layout: post
title: "PlatformIO"
category: post
date: 2016-02-07 22:01:06
tags:
- raspberry
- linux
- flask
---

# Crash course on PlatformIO

[PlatformIO][platformio] is a Python based command line interface to compile and upload code to an Arduino microcontroller. 


## Install platformio

    pip install platformio

## Initialize a Platformio project and specify compilation for Arduino Uno

	#make a directory for the project
	mkdir Sites/triggercamera/testing
	cd Sites/triggercamera/testing
	
	# initialize platformio in the current directory
	platformio init --board uno # arduino uno
	
	#additional boards can be added
	platformio init --board teensy31 # arduino teensy31

## Put treadmill.cpp into platformio /src/ folder

Put .cpp Arduino source code into the /src/ directory

## Tweek platformio.ini

    [env:uno]
    platform = atmelavr
    framework = arduino
    board = uno
    build_flags = -D _expose_interrupts_ #creates compiler directive

	[env:teensy31]
	platform = teensy
	framework = arduino
	board = teensy31

## Compile and upload code

    platformio run #compile arduino code
    platformio run --target upload #compile and upload
    platformio run --target clean #clean project

## Open a serial port with platformio

    #this assumes the Arduino code is listening to serial at baud 115200
    platformio serialports monitor -p /dev/ttyACM0 -b 115200 #a serial port monitor

## Find the correct serial port by listing `/dev/tty*`

    ls /dev/tty*
    
## Specify the correct serial port

    serialStr = '/dev/ttyACM0' #uno

    #serialStr = '/dev/ttyACM0' #teensy on raspberry
    #serialStr = '/dev/tty.usbmodem618661' #teensy at work
    #serialStr = '/dev/tty.usbmodem618661' #teensy?
    #serialStr = '/dev/ttyUSB0' #hand soldered arduino micro (home debian)
    #serialStr = '/dev/tty.usbserial-A50285BI' # hand soldered at work

[platformio]: http://platformio.org