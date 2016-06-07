---
layout: post
title: "Programming an arduino with platformio"
category: post
date: 2016-02-13 22:01:06
tags:
- raspberry
- linux
- arduino
---

This post describes how to install and run [platformio][1] to compile and upload arduino code via a command line interface (CLI). This is a major breakthrough as it allows writing, compiling, and uploading arduino code on an ARM processor (e.g. Raspberry Pi) and on a Debian server. This allows me to program arduino(s) physically connected to headless machines and circumvents all sorts of silliness around the lack of an Arduino IDE for the ARM platform (shame on you arduino).

A major advancement here is that platformio comes preconfigured to talk to boards like the [teensy][4], [eps8266][5], and [node mcu][3].

Running the Arduino IDE on a headless linux box was always a nuisance. I would always have to install, configure and run an X11 server (see [this][6] post) to pull up the graphic interface on a remote (host) machine. 
  
### Install platformio

Platformio is written in python, so all you need is

    sudo pip install -U platformio

### Make a new project directory and initialize an empty project

	mkdir Sites/p5js_plot
	cd Sites/p5js_plot
	platformio init

This will create

  - /src
  - /lib
  - platformio.ini

### Configure platformio.ini with boards

Populate platformio.ini with an uno board

	platformio init --board=uno
	platformio init --board=teensy31
	platformio init --board nodemcuv2

platformio.ini looks something like this

	; Project Configuration File
	; Docs: http://docs.platformio.org/en/latest/projectconf.html
	
	[env:uno]
	platform = atmelavr
	framework = arduino
	board = uno
	
	[env:nodemcu]
	platform = espressif
	framework = arduino
	board = nodemcu
	build_flags = -D LED_BUILTIN=BUILTIN_LED

	[env:teensy31]
	platform = teensy
	framework = arduino
	board = teensy31

	[env:lpmsp430g2553]
	platform = timsp430
	framework = energia
	board = lpmsp430g2553
	build_flags = -D LED_BUILTIN=RED_LED

### Put some arduino code in src/main.cpp

Debugging is not as pretty as with a GUI. The whole arduino gui thing is just overkill in the first place. It is nice to simplify things by returning to a command line.

Remember, we are programming in C++, NOT the arduino language.

~~~
/*
 * Blink
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include "Arduino.h"

void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);
  // wait for a second
  delay(1000);
  // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, LOW);
   // wait for a second
  delay(1000);
}
~~~

### Upload code to arduino

	platformio run --target upload

The first time this is run, platformio automatically downloads the necessary arduino libraries.

### Additional info

[Serial ports][7]
 
	# list serial ports
	platformio serialports list
	# a Miniterm style serial port monitor ('ctrl+]' to quit)
	platformio serialports monitor

	/dev/ttyACM0 #uno and teensy on debian
	/dev/ttyUSB0 #node mcu on debian
	/dev/cu.SLAB_USBtoUART #node mcu on osx

platformio.ini for nodemcu needs to know the serial port

	[env:nodemcuv2]
	platform = espressif
	framework = arduino
	board = nodemcuv2
	upload_port = /dev/ttyUSB0

[1]: http://platformio.org/
[2]: http://p5js.org/
[3]: http://nodemcu.com/index_en.html#fr_54747361d775ef1a3600000f
[4]: https://www.pjrc.com/store/teensy32.html
[5]: https://www.adafruit.com/products/2471
[6]: /post/2015/05/05/X11-on-Raspberry/
[7]: http://docs.platformio.org/en/latest/userguide/cmd_serialports.html

