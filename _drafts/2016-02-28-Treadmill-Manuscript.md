---
layout: post
title: "Treadmill manuscript"
category: post
date: 2016-02-28 22:01:06
tags:
- raspberry
- arduino
- linux
---


Author: Robert Cudmore

#### Abstract

The availability of low cost and open-source microcontrollers like the Arduino Uno (2010) and Linux compatible computers like the Raspberry Pi (2012) coupled with open-source software like Python have the potential to redefine how experiments are designed and data is acquired in research labs.

Here we present a combined Arduino/Raspberry/Python system to control and acquire data for a behavioral experiment where mice are walking on a treadmill.

The treadmill can be driven by a motor or the mouse is allowed to voluntarily walk. The position of the wheel is recorded with a rotary encoder while video is acquired.

Each component of this data acquisition system (motor, rotary encoder, and video) are synchronized, allowing full reconstruction of the experiment both on-line during the experiment and off-line for later data analysis.

Given the low cost of this system, it is possible to scale this system up.

By using open-source hardware and software, this system can be easily and rapidly extended to similar or entirely different experimental configurations.

We couple this system to an existing in vivo two-photon microscope to simultaneously acquire sub-micron resolution images with behavioral data.

This system is a proof-of-principal that rich and complex behavioral data can be acquired in a research laboratory setting using readily available, inexpensive, and open source components.

#### Introduction

Because both the Arduino and Raspberry use general-purpose-input-output (GPIO), they can be easily integrated into existing commercial laboratory equipment.


#### Methods

  ##### Hardware
 
   Arduino
   Raspberry pi
   Raspberry Pi Noir Camera
 
  Stepper motor and motor controller
  Rotary encoder

  ##### Software
 
  Backend written in python

  Arduino code 
 
  ##### Interface
  
  We provide the backend code in Pytohn and it can be controlled from the command line. Using a tool like iPython, it is also possible to make real-time plots.
  
  [write some code to o this]
  
  We also provide a web based interface which communicates with the backend Python code using a Python based Flask server.

  Flask
  SocketIO
  Client-side javascript
  
  Additional interfaces can easily be created using available Python libraries (Tk, Qt, etc) or commercial software (Matlab or Igor Pro).
 
  ##### Mechanical hardware for the treadmill
 
  Treadmill is constructed using low-cost but reasonably precise robotic parts from Actobotics.

  ##### Wiring the system

  Provide a wiring diagram of Arduino and Raspberry
   
  ##### Parts list table

  - Arduino
  - Raspberry Pi
  - Pi Noir Camera
  - IR LEDs

  - Stepper motor
  - Motor controller
  - Rotary encoder
  -Actobotics
    - frames, gears, bearings, etc
   
#### Results

  - Command line interface
  
  - server
   
  - Flask based server and real-time data visualization and analysis through a web-based client.
  
  This allows the system to be controlled and monitored remotely anywhere there is an internet connection. This includes phones and tablets.
  
#### Discussion





