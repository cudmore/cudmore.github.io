---
layout: post
title: "Arduino + stepper motor + rotary encoder + scan image frame clock + serial logging"
category: post
date: 2015-05-24 22:01:06
tags:
- arduino
- python
- raspberry pi
---

Goal here is to make an Arduino do four things simultaneously:

1. Read a rotary encoder
2. Drive a stepper motor
3. Respond to Scan Image (SI) frame clock
4. Log all events to serial

The rotary encoder and stepper motor (1,2) need to be non-blocking. All inputs (1,2,3) need to use low-level interrupts to be 'timing precise' and not get blocked themselves.

Initially I wanted to log all this to Arduino memory but there is not enough on the Arduino Uno. Upgrading to Arduino Mega gives you 4x memory but still not enough. The rotary encoder fires off tons of events and if I hard code events as an array (in Arduino memory), I am limited to about 250 events. Same problem with SI frames, I am limited to about 250 frame timestamps. Arduino ProgMem does not work as it is not writable at runtime. In the future I may get an SD card shield for this?

For now I am having Arduino log all events to serial and am using python code (on a Raspberry Pi) to grab and save all serial events coming from Arduino. I don't like this as I am bound to miss some events or get out of synch due to general flakiness of serial.

###Install Arduino 1.6.x

Don't upgrade the system to Debian Jesse, just pull the Arduino 1.6 packages from Debian Jesse repository.

https://nicohood.wordpress.com/2015/01/24/installing-avr-gcc-4-8-1-and-arduino-ide-1-6-on-raspberry-pi/

His site is moving to [github.com/NicoHood](https://github.com/NicoHood/Arduino-IDE-for-Raspberry). Another person who bailed on Wordpress, hard times for wordpress?

###Motor controller

I am using [EasyDriver](http://www.schmalzhaus.com/EasyDriver/)

###Non blocking stepper motor on arduino
[AccelStepper](http://www.airspayce.com/mikem/arduino/AccelStepper/index.html) Arduino library.


###Rotary encoder
I have a 'Honeywell 600-128-cbl'. Looking at wires as they come out of encoder...

- green - Ground
- yellow -  'A' out -->> arduino 0
- orange - 'B' out -->> arduino 1
- red - 5 Vdc

Pinouts are in [.pdf on farnell website](http://www.farnell.com/datasheets/1712854.pdf)


Mount with nut and lockwasher
- Hex Mount Nut: 3/8 in x 32
- Internal Tooth Lockwasher
    
###Rotary encoder library

A non-blocking rotary encoder library for Arduino is made by [pjrc](http://www.pjrc.com/teensy/td_libs_Encoder.html).


###Setting arbitrary interrupts on Arduino

By default the Arduino Uno has low level interrupts on input pins 2 and 3. I need more interrupts. You can upgrade your Arduino board or just set low level interrupts on any input pin. I am setting A0/A1/A2 to accept [low level interrupts](http://www.geertlangereis.nl/Electronics/Pin_Change_Interrupts/PinChange_en.html)


###Plotting sensor data from arduino

This is tricky as parsing incoming serial data is slow. It is slow on any operating system and with any CPU chip including Pentium i7 running OSX or Window, Arm processor on Raspberry Pi. The serial parsing/reading eventually finishes but to get a legitimate real-time plot requires buffering a number of values and plotting them in a batch. This is particularly important for the high bandwidth of the rotary encoder.

I tried three different options and dedicating myself to pyqtgraph...

- [Matplotlib](http://matplotlib.org). Too slow and plots are inherently non interactive (like Matlab).
- [Processing](https://processing.org). Very simple to implement, good for prototyping, very powerful Java based code. In the end I want to use Python so I am ditching it for final production.
- [PyQtGraph](http://www.pyqtgraph.org). Python based and designed to plot within an application. HIghly interactive.


####Good code for python matplotlib

    https://www.lebsanft.org/?p=48

####Processing on the pi

Installing Processing on the PI is a little tricky.

http://cagewebdev.com/index.php/raspberry-pi-running-processing-on-your-raspi/

####pyqtgraph
    sudo pip install pyqtgraph
    

        
###Gotchas
 - Don't connect pin 0 on Arduino, you will get arduino error
    avrdude stk500_getsync(): not in sync
 
###Put Arduino libraries in
    /usr/share/arduino/libraries/
  
##Links
  
- AccellStepper Arduino library  
http://www.airspayce.com/mikem/arduino/AccelStepper/index.html

- Non blocking rotary encoder library for Arduino  
http://www.pjrc.com/teensy/td_libs_Encoder.html

- Setting any pin as a low level interrupt on Arduino  
http://www.geertlangereis.nl/Electronics/Pin_Change_Interrupts/PinChange_en.html

- easy driver motor controller  
http://www.schmalzhaus.com/EasyDriver/
http://www.schmalzhaus.com/EasyDriver/Examples/EasyDriverExamples.html

- pinouts for 'Honeywell 600-128-cbl' rotary encoder  
http://www.farnell.com/datasheets/1712854.pdf

- EasyDriver Tutorials  
http://bildr.org/2012/11/big-easy-driver-arduino/
http://bildr.org/2012/11/big-easy-driver-arduino/

- [not useful] A small fork of AccelStepper v1.3 with AF_motor (Adafruit motor shield) support  
https://github.com/adafruit/AccelStepper

- [Matplotlib](http://matplotlib.org).
- [Processing](https://processing.org).
- [PyQtGraph](http://www.pyqtgraph.org).
