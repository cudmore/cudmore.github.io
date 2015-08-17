---
layout: post
title: "Plotting with bokeh on the Raspberry Pi"
category: post
date: 2015-03-05 22:01:06
tags:
- bokeh
- flask
- python
- raspberry pi
---

Goal is to get plotting with bokeh on the Raspberry Pi.

- Install continuum anaconda python distribution
- Install bokeh plotting and get a plot server running
- be able to run bokeh examples

[UPDATE August 16, 2015]
[THIS IS NOT WORKING ... REWRITING]

- don't install miniconda, just use stock raspian pytohn

```python
# this takes > 1 hour on a Raspberry Pi Model B !!!
# most of the time is spent in gcc cc1 command
sudo pip install pandas --upgrade 
# after > 1 hour I get an error
# Successfully installed pandas python-dateutil pytz
# OSError: [Errno 39] Directory not empty: '/home/pi/build/pytz'
# I am ignoring this pytz error (something to do with timezone library???)
#
# now i am sidetracked
sudo pip install ipython
# ipython seems ok
#
# this next one may take awhile, started at 1:50pm
sudo pip install bokeh  
# seems ok, can import pandas in python but it gives error
#
#    /usr/local/lib/python2.7/dist-packages/pandas/computation/expressions.py:21: UserWarning: The installed version of numexpr 2.0.1 is not supported in pandas and will be not be used
#    The minimum supported version is 2.1
#
# fixed error with (hopefully does not cause other problems)
sudo pip install numexpr --upgrade
```

[ORIGINAL POST STARTS HERE]

###Install miniconda
	pi@pi40 ~ $ wget http://repo.continuum.io/miniconda/Miniconda-3.5.5-Linux-armv6l.sh
	pi@pi40 ~ $ bash Miniconda-3.5.5-Linux-armv6l.sh 

	Miniconda will now be installed into this location:
	/home/pi/miniconda

	  - Press ENTER to confirm the location
	  - Press CTRL-C to abort the installation
	  - Or specify an different location below

	[/home/pi/miniconda] >>> 
	PREFIX=/home/pi/miniconda
	installing: python-2.7.7-0 ...
	installing: openssl-1.0.1h-0 ...
	installing: pycosat-0.6.1-py27_0 ...
	installing: pyyaml-3.11-py27_0 ...
	installing: requests-2.3.0-py27_0 ...
	installing: yaml-0.1.4-0 ...
	installing: conda-3.5.5-py27_0 ...
	Python 2.7.7 :: Continuum Analytics, Inc.
	creating default environment...
	installation finished.
	Do you wish the installer to prepend the Miniconda install location
	to PATH in your /home/pi/.bashrc ? [yes|no]
	[no] >>> yes

	Prepending PATH=/home/pi/miniconda/bin to PATH in /home/pi/.bashrc
	A backup will be made to: /home/pi/.bashrc-miniconda.bak


	For this change to become active, you have to open a new terminal.

	Thank you for installing Miniconda!

###Make sure numpy and pandas is correct

> pip install numpy --upgrade  
> pip install pandas --upgrade  

###Install bokeh
In general 'conda install bokeh' does not work on Pi, bokeh is not in repo?

> pip install bokeh  

For a list of required packages, see http://bokeh.pydata.org/en/latest/tutorial/quick_install.html  

	from: http://bokeh.pydata.org/en/latest/tutorial/quick_install.html
	Ideally, you should have the following libraries installed:

	NumPy
	Flask
	Redis
	Requests
	gevent
	gevent-websocket
	Pandas


###Currently installed with pip

	pi@pi40 ~ $ pip freeze
	Flask==0.10.1
	Flask-Markdown==0.3
	Flask-Misaka==0.3.0
	Flask-SocketIO==0.5.0
	Jinja2==2.7.3
	Markdown==2.6
	MarkupSafe==0.23
	PyYAML==3.11
	Pygments==2.0.2
	RPi.GPIO==0.5.11
	Werkzeug==0.10.1
	backports.ssl-match-hostname==3.4.0.2
	bokeh==0.8.1
	colorama==0.3.3
	conda==3.5.5
	gevent==1.0.1
	gevent-socketio==0.3.6
	gevent-websocket==0.9.3
	greenlet==0.4.5
	ipython==2.1.0
	itsdangerous==0.24
	misaka==1.0.2
	nose==1.3.0
	numpy==1.9.2
	pandas==0.15.2
	psutil==2.2.1
	pycosat==0.6.1
	pystache==0.5.4
	python-dateutil==2.4.1
	pytz==2014.10
	pyzmq==14.5.0
	requests==2.3.0
	six==1.9.0
	tornado==4.1
	websocket==0.2.1
	wsgiref==0.1.2

###Grab some example plots from bokeh github

The bokeh example plots are at:

> https://github.com/bokeh/bokeh/tree/master/examples/plotting/server

###Run the bokeh-server
Remember, this make temporary files in directory you run it in.

--ip 0.0.0.0 will redirect the server to your external IP, in my case http://192.168.1.40:5006  
> 
> bokeh-server --backend=memory --ip 0.0.0.0

	pi@pi40 ~/bokeh_examples $ bokeh-server --backend=memory --ip 0.0.0.0
	No module named scipy

	    Bokeh Server Configuration
	    ==========================
	    python version : 2.7.8
	    bokeh version  : 0.8.1
	    listening      : 0.0.0.0:5006
	    backend        : memory
	    python options : debug:OFF, verbose:OFF, filter-logs:OFF, multi-user:OFF
	    js options     : splitjs:OFF, debugjs:OFF
	    
	/home/pi/miniconda/lib/python2.7/site-packages/bokeh/server/blaze/__init__.py:19: UserWarning: could not import multiuser blaze server No module named blaze.  This is fine if you do not intend to use blaze capabilities in the bokeh server
	  warnings.warn(msg)

###Example plots I have working

line_animate.py

	# The plot server must be running
	# Go to http://localhost:5006/bokeh to view this plot

	import time

	import numpy as np

	from bokeh.plotting import *

	N = 80

	x = np.linspace(0, 4*np.pi, N)
	y = np.sin(x)

	output_server("line_animate")

	p = figure()

	p.line(x, y, color="#3333ee", name="sin")
	p.line([0,4*np.pi], [-1, 1], color="#ee3333")

	show(p)

	renderer = p.select(dict(name="sin"))
	ds = renderer[0].data_source

	while True:
	    for i in np.hstack((np.linspace(1, -1, 100), np.linspace(-1, 1, 100))):
	        ds.data["y"] = y * i
	        cursession().store_objects(ds)
	        time.sleep(0.05)

###Now use Flask + bokeh to generate a single html page (no bokeh-server)
- eventual goal here is to have Flask server inject new data (via socketio) into html page with bokeh plot by modifying x/y data with javascript (on the client)
- simple example that works: https://github.com/bokeh/bokeh/tree/master/examples/embed/simple  
- more complex: https://github.com/bokeh/bokeh/tree/master/examples/embed/spectrogram

###Links  
- http://bokeh.pydata.org/en/latest/index.html  
- http://docs.continuum.io/anaconda/install.html  
