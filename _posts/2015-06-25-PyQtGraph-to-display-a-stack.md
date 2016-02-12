---
layout: post
title: "pyqtGraph to display a .tif stack"
category: post
date: 2015-08-14 22:01:06
tags:
- python
---

This will display a 3D .tif stack where slices can be viewed and contrast set.

#### Install libraries

	pip install pyqtgraph
	pip install tifffile

#### Python code

	import pyqtgraph as pg
	import tifffile
	tif = tifffile.TiffFile('Desktop/zyF4107_d1_s0_ch1.tif')
	images = tif.asarray()
	pg.image(images)

#### To Do
  - Not sure how this works for 2 channels.
  - See how easy it is to plugin custom python code into PyQtGraph.
    1. Remove the right contrast slider and bottom slice slider.
    2. Swap mouse wheel from zooming image to scrolling slices.
    3. Overlay 3D annotations that are masked. Appear and disappear as a function of slices.
    4. Select a 3D annotation.
  
#### Links

  - [PyQtGraph](http://www.pyqtgraph.org)
  - TiffFile is provided by [Christoph Gohlke](http://www.lfd.uci.edu/%7Egohlke/) and is [here](http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html)
	
<IMG SRC="/images/example-pyqtgraph.png" width=800>
