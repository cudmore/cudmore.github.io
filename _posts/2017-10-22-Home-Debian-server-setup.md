---
layout: post
title: "Home Debian server setup
category: post
date: 2017-10-22 00:00:01
tags:
- debian
---

### Homeassistant

Web interface is at: http://192.168.1.200:8123

For setup, see: https://home-assistant.io/docs/installation/virtualenv/

Application is in /srv/homeassistant/

Added a user /home/homeassistant

Main configuration file is: /home/homeassistant/.homeassistant/configuration.yaml

To edit configuration.yaml, switch user: sudo su -s /bin/bash homeassistant

To run homeassistant (from my normal account): sudo -u homeassistant -H /srv/homeassistant/bin/hass

todo: learn how to run this crap at startup

My homeassistant is subscribing and getting packets from mosquitto mqtt server with the following in configuration.yml

	mqtt:
	  broker: 192.168.1.200       
	  #username: your_username
	  #password: your_password

	sensor 1:
	  platform: mqtt
	  name: "Temperature"
	  state_topic: "nodemcu1/temperature"
	  qos: 0
	  unit_of_measurement: "ºC"

	sensor 2:
	  platform: mqtt
	  name: "Humidity"
	  state_topic: "nodemcu1/humidity"
	  qos: 0
	  unit_of_measurement: "%"

	sensor 3:
	  platform: mqtt
	  name: "Light"
	  state_topic: "nodemcu1/light"
	  qos: 0
	  unit_of_measurement: "%"

### Python3 is in env py36

To get homeassistant working, installed virtual env 'py36' for python 3.6 install

See: https://conda.io/docs/user-guide/tasks/manage-python.html

    conda create -n py36 python=3.6 anaconda
    
Activate environment

    source activate py36
    
Deactivate environment

    source deactivate
    
### MQTT

See [MQTT post][1] on how to start/stop

Basically

    sudo systemctl start mosquitto
    sudo systemctl stop mosquitto

MQTT is running at 192.168.1.200:1883

Mosquitto config is in: /etc/mosquitto/mosquitto.conf

My node mcu is

### Node MCU temperature sensor

This info is directly from router 192.168.1.1

    192.168.1.3
    ESP_D38E41
    18:FE:34:D3:8E:41
    
### temperature server

is in: ~/Sites/temperatureserver/app.py

run it manually with screen (too much of a pain to get it to run on boot)

once running, is at: http://192.168.1.200:5000
or: cudmore.duckdns.org:5000

Remember, duckdns only works because I (1) port forward to .200 on router and (2) run some sort of synch software (from duckdns people) to notify their servers when my dynamic IP changes

temperature server subscribes to the MQTT server and listens on broker channel '#'

    paho.Client().subscribe('#', 0)
    

These are my mqtt broker channels

	if msg.topic == 'nodemcu1/light':
		nodemcu1_light = str(msg.payload)
		#print '    nodemcu1_light=', nodemcu1_light
	if msg.topic == 'nodemcu1/temperature':
		nodemcu1_temperature = str(msg.payload)
		#print '    nodemcu1_temperature=', nodemcu1_temperature
	if msg.topic == 'nodemcu1/humidity':
		nodemcu1_humidity = str(msg.payload)
		#print '    nodemcu1_humidity=', nodemcu1_humidity
	
	if msg.topic == 'nodemcu2/temperature':
		nodemcu2_temperature = str(msg.payload)
	if msg.topic == 'nodemcu2/humidity':
		nodemcu2_humidity = str(msg.payload)

    
[1]: /post/2016/01/19/MQTT/
