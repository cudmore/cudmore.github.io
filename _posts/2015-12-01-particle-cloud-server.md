---
layout: post
title: "particle cloud server"
category: post
date: 2015-12-01 22:01:06
tags:
- osx
- linux
- arduino
---

#### This is not working ... as of 12/3/2015 I will just wait for the particle people to update the particle-server with better support for the photon (it is really designed for the particle.

The paticle photon is a great little wifi enabled arduino. The only problem I have is that all read/write using its REST API requires internet acces to a particle.io account. To get around this, you can run a particle cloud server locally.

I am doing all of this on a Debian Jessie server.

#### install git
~~~
sudo apt-get install git
~~~

#### install nodejs (use su to enter su/root)
Following: https://github.com/nodesource/distributions

~~~
curl -sL https://deb.nodesource.com/setup_4.x | bash -
apt-get install -y nodejs
~~~

#### Install particle cli
Following: https://github.com/spark/particle-cli

~~~
sudo npm install -g particle-cli
~~~

#### Install particle cloud server
Following: https://github.com/spark/spark-server/

~~~
git clone https://github.com/spark/spark-server.git
cd spark-server
npm install
node main.js
~~~

'node main.js' produced

~~~
-------
No users exist, you should create some users!
-------
connect.multipart() will be removed in connect 3.0
visit https://github.com/senchalabs/connect/wiki/Connect-3.0 for alternatives
connect.limit() will be removed in connect 3.0
Starting server, listening on 8080
static class init!
core keys directory didn't exist, creating... /home/cudmore/spark-server/core_keys
Creating NEW server key
Loading server key from default_key.pem
set server key
server public key is:  -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAz3oPu+QsNdQaVgk+e4nS
zmTxop7vVamrKdIpio04yoY9pKPmkORAmM0VdFgYKinn094cHERm+LFdDhSAtWtn
TIErdd3o2ntoyZoYLC30Q2Mwvb+AzvGRcrW7jk+72up6YbXMZi2lhRs9M5Qe7use
mXy96PiRP7tYD+Yj+k0t3bDF+lfiWHuuG/yV2/hQaQ8ADfqtWvX4XyLMC9XS2m94
HhFy83sWPcRcB7BZUr1A8w503vB+gZWlt8W+uPlbUmbF+P8LzZmE4Twn87EcMeTB
qGvBxjWypHF95jDzZCie5/glZtunmH905Lb12y1eWLY29KPPk8BcpIzPJ5xc8mKk
gQIDAQAB
-----END PUBLIC KEY-----

Your server IP address is: 192.168.1.200
server started { host: 'localhost', port: 5683 }

~~~

#### Continue setting up particle server
Install [dfu-utils](http://dfu-util.sourceforge.net)

~~~
	# git clone git://git.code.sf.net/p/dfu-util/dfu-util
	sudo apt-get build-dep dfu-util
	sudo apt-get install libusb-1.0-0-dev
~~~

But that did not work so i did

~~~
sudo apt-get upgrade dfu-util
~~~

This updated a boat load of things including jre and owncloud (leaving it in maintenance mode). To turn owncloud maintenance mode off, follow [this](https://doc.owncloud.org/server/8.0/admin_manual/maintenance/enable_maintenance.html) and edit /var/www/owncloud/config/config.php and set 'maintenance' => false,'. The next time I logged into my owncloud server it triggered an update to 8.2.1


Try again with particle photon plugged in via usb

Still following: https://github.com/spark/spark-server/


~~~
particle keys server default_key.pub.pem 192.168.1.10
~~~

gave

~~~
cudmore@debian:~/spark-server$ sudo particle keys server default_key.pub.pem 192.168.1.200
running dfu-util -l
Found DFU device 2b04:d006
checking file  default_key.pub192_168_1_200.der
spawning dfu-util -d 2b04:d006 -a 1 -i 0 -s 2082 -D default_key.pub192_168_1_200.der
dfu-util 0.8

Copyright 2005-2009 Weston Schmidt, Harald Welte and OpenMoko Inc.
Copyright 2010-2014 Tormod Volden and Stefan Schmidt
This program is Free Software and has ABSOLUTELY NO WARRANTY
Please report bugs to dfu-util@lists.gnumonks.org

dfu-util: Invalid DFU suffix signature
dfu-util: A valid DFU suffix will be required in a future dfu-util release!!!
Opening DFU capable USB device...
ID 2b04:d006
Run-time device DFU version 011a
Claiming USB DFU Interface...
Setting Alternate Setting # 1 ...
Determining device status: state = dfuIDLE, status = 0
dfuIDLE, continuing
DFU mode device DFU version 011a
Device returned transfer size 4096
DfuSe interface name: "DCT Flash   "
Downloading to address = 0x00000822, size = 1024
Download	[=========================] 100%         1024 bytes
Download done.
File downloaded successfully
Okay!  New keys in place, your device will not restart.
~~~
