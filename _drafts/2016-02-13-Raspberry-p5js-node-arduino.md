---
layout: post
title: "Raspberry + p5.js + node + arduino"
category: post
date: 2016-02-13 22:01:06
tags:
- raspberry
- linux
- arduino
---

Goal is to read analog input from arduino and plot it in a browser using p5.js.

### Background

Following this tutorial

https://itp.nyu.edu/physcomp/labs/labs-serial-communication/lab-serial-input-to-the-p5-js-ide/

And this github

https://github.com/vanevery/p5.serialport

### Update the pi

    sudo apt-get update
    sudo apt-get upgrade
    
### Download and install [node][1]

~~~
wget https://nodejs.org/dist/v4.3.0/node-v4.3.0-linux-armv7l.tar.xz
tar -xvf node-v4.3.0-linux-armv7l.tar.gz 
cd node-v4.3.0-linux-armv7l
sudo cp -R * /usr/local/
~~~

check the version of node with

    node -v
    v4.3.0


that did not work. serialport does not seem to work with node 4.x

found node-v0.12.7-linux-arm-v7.tar.gz

http://conoroneill.net/node-v01040-and-v0127-for-arm-v7-raspberry-pi-2-banana-pi-odroid-c1-available/


first try to upgrade

    npm update ws
    npm update serialport
    
install some node libraries

    sudo npm install ws
    sudo npm install serialport


[1]: https://nodejs.org/en/download/