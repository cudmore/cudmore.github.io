---
layout: post
title: "Raspberry Pi video controller"
category: post
date: 2015-03-20 22:01:06
tags:
- raspberry pi
- data acquisition
---

This is a video server running on a raspberry Pi Linux computer. It provides a web interface to stream and record video.


### What it does

  - **Arm** - Start video recording when a TTL is received. Hook up the ScanImage frame clock to the Pi and this will start a video recording at the start of each stack or timeseries. 
  - **Record** - Record a one time video. 
  - **Stream** - Stream the video to your web browser so you can see a live feed.
  - **Stop** - Stop any video streaming or recording.
  - **IR On/Off** - Turn one set of LEDs on/off. The brightness of the LED is set with the slider. This is usually hooked up to a bank of IR LEDs.
  - **White On/Off** - Turn one set of LEDs on/off (usually hooked up to White LEDs)
  - **Message** - Text entered in the 'Messages' field are saved to a text file with timestamps.
  - Provides real-time feedback with elements/objects within the webpage updated without reloading. Some examples are: the time of day, the last ScanImage frame number, current log file, temperature, humidity, etc.

### Interface
<IMG SRC="/images/example-iosserver.png" width=700 align=CENTER>

### How it works
The server is pure python running on the Pi. It uses the web framework [Flask][1]. Once the web page is loaded by a client browser(you), any objects within the webpage can be updated in real-time using [flask-socket-io][2]. This can be done without refreshing the entire webpage. The layout and interface objects are using [Bootstrap][3].


### Required Hardware
  - [Raspberry Pi][4]
  - [Raspberry Pi Camera][4], the IR version is called 'NOIR'.
  
### Installation:

- [I need to make a GitHub repository with the python source code]
- [I need to write out how I install this, my original and pretty useless notes are [here](http://cudmore.github.io/post/2015/03/15/Installing-mjpg-streamer-on-a-raspberry-pi/)]
  
### Running the server

    sudo python iosserver.py

  This will tell you the IP adress you use to login to the server.

### Connecting to the server

  Just point any browser to the server address.

    http://192.168.1.60:5000
    
## Extra Details

### The internet of things

Python code running on any other internet-connected device can 'inject' values into the iosserver and they will show up in real-time inside all client browsers. Here is example code on another Pi that has its own temperature and humidity sensor.

~~~python
# send to iosserver
import requests
try:
	payload = {'timestamp': thisTimestamp, 'insideTemp': temp, 'insideHum': hum, 'outsideTemp' : outsidetemp, 'outsideHum' : outsidehumidity}
	r=requests.get('http://192.168.1.60:5000/_add_numbers', params=payload)
	print 'sent to 192.168.1.60 !!!'
	print payload
except:
	print '-------- error sending to iosserver ---------'
~~~

The iosserver receives this GET request with a little function decorator.

~~~python
@app.route('/_add_numbers')
def add_numbers():
    timestamp = request.args.get('timestamp', '') # defaults to ''
    insideTemp = request.args.get('insideTemp', '')
    insideHum = request.args.get('insideHum', '')
    outsideTemp = request.args.get('outsideTemp', '')
    outsideHum = request.args.get('outsideHum', '')
    print 'timestamp=', timestamp
    # myVideo is another python class that handles all runtime
    # it is not detailed in this example
    myVideo.insideTemp = timestamp + ' ' + insideTemp
    myVideo.insideHum = insideHum
    myVideo.outsideTemp = outsideTemp
    myVideo.outsideHum = outsideHum
    print 'add_nummbers() received ', timestamp, ' ', insideTemp, ' ', insideHum, ' ', outsideTemp, ' ', outsideHum
    return ''
~~~

There are a few more steps including some javascript and html. This is not a Flask or Socket-IO tutorial. Have a look a [socket-io for Flask][2].

[1]: http://flask.pocoo.org
[2]: https://flask-socketio.readthedocs.org/en/latest/
[3]: http://getbootstrap.com
[4]: https://www.raspberrypi.org/products/
