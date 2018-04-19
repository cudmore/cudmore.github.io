---
layout: post
title: "Raspberry startup tweet"
category: post
date: 2017-10-27 00:00:01
tags:
- linux
- raspberry
---

Have a Raspberry send a tweet with its IP when it boots. This is incredibly useful when your Pi is headless with no monitor. There are tons of tutorials on this including one at [instructables][2] and another at [opensource][3].

This is what you will get

<blockquote class="twitter-tweet" data-lang="en"><p lang="it" dir="ltr">triggercamera1 10.16.80.238 2016-10-20 18:04:40</p>&mdash; cudmore.io (@cudmore_io) <a href="https://twitter.com/cudmore_io/status/789225852013834244?ref_src=twsrc%5Etfw">October 20, 2016</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Used to send [email at boot][5] but I can't get the Pi to send email via gmail any more?


### Create and configure a twitter app

Go to [apps.twitter.com][1] and make a twitter app. You will need a normal twitter account. Make sure you turn on read/write access. Once that is done, note down all the keys.

 - Consumer Key (API key)
 - Consumer Secret (API Secret)
 - Access Token
 - Access Token Secret

### install tweepy (could also use twython)

	pip install tweepy

### Write a python script

Lets call it `startup_tweeter.py`. See Github Gist below.

### Make the python script run at boot

Make script executable

    chmod u+x startup_tweeter.py

Edit crontab

	sudo crontab -e
	
Add one line at the end of crontab

	@reboot (sleep 10; python /home/pi/startup_tweeter.py)

### Python script to tweet IP

This is taken from [RasPi.tv][4]

<script src="https://gist.github.com/cudmore/7c909d2c51c3315c7b03e1485d0ad25a.js"></script>


[1]: http://apps.twitter.com
[2]: http://www.instructables.com/id/How-to-Send-Tweets-From-Your-Raspberry-Pi/
[3]: https://opensource.com/article/17/8/raspberry-pi-twitter-bot
[4]: http://raspi.tv/2013/how-to-create-a-twitter-app-on-the-raspberry-pi-with-python-tweepy-part-1
[5]: http://www.robertcudmore.org/blog/?p=60
