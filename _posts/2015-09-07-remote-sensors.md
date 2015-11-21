---
layout: post
title: "remote sensors"
category: post
date: 2015-09-07 22:01:06
tags:
- arduino
- raspberry
- flask
---

A distributed client sensor to data server network.

###This is kind of bullshit

###Background

 - Client sensors transmit to data server(s) via http/rest interface.
 - Data servers receive client sensor data and log it to a file.
 - Any number of client sensors can transmit to any number of data servers as long as the client sensors know the IP address of the servers.
 - Data servers are agnostic to the identity of the client sensors. Each client sensor embeds its identity into the data sent to the server.

###Interface

 - Point your browser to the webpage [http://cudmore.duckdns.org:5000](http://cudmore.duckdns.org:5000)

###Hardware
 - Sensors clients can run on either a Raspberry Pi or an Arduino.
 - Sensors clients can include: temperature, motion detection, light levels, or a camera.
 - Data servers run on Linux Debian Jessie, OS X, or Raspberry Raspian.
 - Both sensor clients and data servers are running Python. If sensor client is on Arduino, it runs Arduino code.
 - Date servers run [Flask](http://flask.pocoo.org) to serve the webpage and use [socket-io](https://flask-socketio.readthedocs.org/en/latest/) for realtime updates of pages served.

###Mix-n-match
 - A client sensor can also be running a data server. For example, a Raspberry Pi with a motion sensor client can also have a data server to receive motion events to trigger an image capture.
 - Alternatively, a sensor client could have two sensors: a motion detector and a camera. In this case, motion would trigger an image capture and then transmit this as two events to a data server (a motion detection timestamp and an image).

###'Real world' input
 - Data servers can receive input from people. For example, a button to request a sensor client to read the current temperature or to take an image. In this senario, the sensor client also needs a data server to receive the button commands.

###API

```
/bokeh
   plot with bokeh
   
/images/a
   plot with matplotlib
   
/keen
   plot with keen (pulls data from keen server)
   
/system
   the type of system the server is running on 
   
```