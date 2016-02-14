---
layout: post
title: "Monitoring mice in their home cage"
category: post
date: 2014-02-14 22:01:06
tags:
- flask
- python
- raspberry pi
- data acquisition
---

[Aug 4, 2014, updated]
[March 2015, moved to cudmore.github.io]

## Goal
- videotape mice in their home cage.

### Parts
#### Computer
<UL>
<LI>Raspberry Pi, Model B 512MB RAM, [Adafruit 998](http://www.adafruit.com/products/998) target="_blank">Adafruit 998</a></li>
	<li>4 GB SD Card, <a href="http://www.adafruit.com/products/102" target="_blank">Adafruit 102</a></li>
	<li>USB 2 Wifi Dongle (802.11b/g/n), <a href="http://www.adafruit.com/products/814" target="_blank">Adafruit, 814</a></li>
	<li>USB 2 Powered Hub, 5V 2A, <a href="http://www.adafruit.com/products/961" target="_blank">Adafruit, 961</a></li>
	<li>USB 2 hard-drive, Old laptop drive with a SATA to USB 2 connector</li>
	<li>5V 1A AC to DC converter, <a href="http://www.adafruit.com/products/501" target="_blank">Adafruit, 501</a></li>
</ul>

<h4>Video</h4>
<ul>
	<li>Raspberry Pi NoIR camera, <a href="http://www.adafruit.com/products/1567" target="_blank">Adafruit, 1567</a></li>
	<li>12" flex cable for Raspberry Pi NoIR Camera, <a href="http://www.adafruit.com/products/1648" target="_blank">Adafruit, 1648</a> (24", <a href="https://www.adafruit.com/products/1731" target="_blank">Adafruit 1731</a>)</li>
	<li>4x Right-angle 1/2" post clamps, <a href="http://search.newport.com/?q=*&amp;x2=sku&amp;q2=CA-1" target="_blank">Newport CA-1</a></li>
	<li>Mini Ball Head, <a href="http://www.bhphotovideo.com/c/product/221096-REG/Giottos_MH1004_320_MH_1004_Mini_Ball.html" target="_blank">B&amp;H Giottos MH1004</a></li>
	<li>1/2" hollow aluminum tubes, these are cheap and easily cut with hack-saw, <a href="http://www.homedepot.com/p/Allied-Tube-Conduit-1-2-in-x-10-ft-Electric-Metallic-Tube-Conduit-101543/100400405" target="_blank">Home Depot</a></li>
</ul>

<strong>Lights</strong>
<ul>
	<li>2x LED Driver, 12VDC 700 MA, <a href="https://www.superbrightleds.com/moreinfo/led-drivers/700ma-constant-current-led-driver/1323/3045/" target="_blank">SuperBrightLeds, CCD-700</a></li>
	<li>4x LED PCB,  <a href="http://www.superbrightleds.com/moreinfo/bare-circuit-boards/universal-4-led-miniature-wedge-base-pcb-mled-pcb/403/1387/" target="_blank">SuperBrightleds, MLED-PCB, 84778101387</a></li>
	<li>2x Mosfet PCB, <a href="https://www.sparkfun.com/products/10256" target="_blank">Sparkfun, COM-10256</a></li>
	<li>LED - Super Bright White (25 pack)</li>
	<li>LED - Infrared 850nm (25 pack), <a href="https://www.sparkfun.com/products/9854" target="_blank">Sparkfun COM-09854</a></li>
	<li>LED - Infrared 950nm (25 pack), <a href="https://www.sparkfun.com/products/10557" target="_blank">Sparkfun COM-10557</a></li>
	<li>2x LED Light Bar - White (SMD), <a href="https://www.sparkfun.com/products/12014" target="_blank">Sparkfun, COM-12014</a></li>
	<li>Light Holders,<b> </b>25 lb circular magnets, 3 foot threaded rods, screws, washers (Ace Hardware)</li>
</ul>

<h4>Running Wheels</h4>
<ul>
	<li>Empty running wheels from <a href="http://www.med-associates.com/product/low-profile-wireless-running-wheel-for-mouse/" target="_blank">Med Associates</a> (find cheaper solution)</li>
	<li>2 Hall Effect sensors per wheel (Optek/TT O090U), <a href="http://www.mouser.com/ProductDetail/Optek-TT-electronics/OH090U/?qs=MYMjFsmMg9Zxhz344sS0jg==" target="_blank">Mouser 828-OH090U</a></li>
</ul>

<h4>Miscellaneous Sensors</h4>
<ul>
	<li>Visible light sensor (Vishay, TEPT5600), <a href="http://www.mouser.com/ProductDetail/Vishay/TEPT5600/?qs=%2fha2pyFadujUHPassviAP51fh4B6FFdxq%2fQn0JoB63RFxPBe7%2ffCXA%3d%3d" target="_blank">Mouser 782-TEPT5600</a></li>
	<li>IR sensor (Vishay BPW83), <a href="http://www.mouser.com/ProductDetail/Vishay/BPW83/?qs=%2fha2pyFaduiEcAuMy5rpt15ObB2haiIvhq3aASHM7R0%3d" target="_blank">Mouser 782-BPW83</a></li>
	<li>Temperature and Humidity Sensor (AM2302 wired DHT22), <a href="http://www.adafruit.com/products/393" target="_blank">Adafruit 393</a></li>
</ul>

<strong>Acquisition Software (</strong>Python scripts running in Pi)

Script 1:
<ul>
	<li>Acquires sequential 5 minute videos and save each to a timestamped .h264 file.</li>
</ul>

Script 2:
<ul>
	<li>Turns IR and White lights on and off, uses time-of-day from Raspberry Linux.</li>
	<li>Reads from IR and visible light sensors to check light levels and sends an email if either IR or white lights burn out.</li>
	<li>Reads temperature and humidity.</li>
	<li>Reads wheel turn events using low level GPIO callbacks to get more accurate time.</li>
	<li>Logs all of this to text file locally on Raspberry.</li>
	<li>Pushes all of this to online web server so I can check if the mice have been running. <del>Remote webserver has a PHP script to accept and save name/value pairs of data</del>. Now using mySQL on external web server.</li>
</ul>

<strong>Software Analysis</strong>
<ul>
	<li>Python/OpenCV motion detection using a modified version of <a href="http://derek.simkowiak.net/motion-tracking-with-python/" target="_blank">this</a> (Thanks to Derek Simkowiak). Motion detection does not run on Pi, runs offline on desktop/laptop (OS X)</li>
	<li>In future, write in C++/OpenCV using <a href="http://sundararajana.blogspot.com/2007/05/motion-detection-using-opencv.html" target="_blank">this</a>.</li>
	<li><a title="Setting up Python, OpenCV and ffmpeg in OSX" href="http://www.robertcudmore.org/blog/?p=183" target="_blank">How to install Python/OpenCV/ffmpeg on OSX</a></li>
	<li>Another project to monitor a hamster in their cage, <a href="http://www.raspberrypi.org/learning/hamster-party-cam/">the hamster party-cam</a> (from the Raspberry people).</li>
</ul>

=====================================================================
<h3>Wish List</h3>
<strong>Sensors</strong>
<ul>
	<li><del>Temperature and Humidity sensor, <a href="http://www.adafruit.com/products/393" target="_blank">Adafruit, 393</a>, $15</del></li>
	<li><del>Upgrade temperature/humidity to something like, <a href="http://www.adafruit.com/products/1293" target="_blank">Adafruit 1293</a>, $30, no tutorials 2/14/14</del></li>
</ul>
<strong>Camera Holder</strong>
<ul>
	<li><del>Right-angle 1/2" post clamps, <a href="http://www.thorlabs.com/thorProduct.cfm?partNumber=RA90" target="_blank">Thor Labs, RA90</a> (google image search for 'Right Angle Clamp rod'). Will order Newport right-angle post clamp, Newport <a href="http://search.newport.com/?q=*&amp;x2=sku&amp;q2=CA-1" target="_blank">CA-1</a>. In general, it seems that any kind of post system with clamps, junctions, and T's triples in price as soon as the post/rod diameter goes below 1/2". Because I need many of these post clamps, 3-4 for camera and 3-4 for lights) I will stick with the 1/2" variety. My choice to go with Newport is based on <a href="http://mousevr.blogspot.com/2011_09_01_archive.html" target="_blank">this</a> comment.</del></li>
	<li><del>1/2" aluminum OR wood tubes/dowels</del></li>
	<li><del>12" flex cable for Raspberry Pi NoIR Camera, <a href="http://www.adafruit.com/products/1648" target="_blank">Adafruit, 1648</a></del></li>
</ul>
=====================================================================
<h3>Notes</h3>
Temp/Humidity Sensor (DHT22) spits out readings once per second (fine) and does it fast (not fine). On Raspberry Pi this requires some C code to read 'bit-banged' sensor output. See <a href="http://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging" target="_blank">Adafruit</a>.

The <a href="http://www.adafruit.com/products/1293" target="_blank">AM2315</a> is a more accurate temperature/humidity sensor, and data comes in via I2C. This particular sensor has a fixed address.

The Pi NoIR camera is just the standard Pi camera with the IR filter removed. Right now there are no detailed specs on the nm sensitivity of the NoIR camera, the IR filter or the original camera for that matter. According to the <a href="http://elinux.org/Rpi_Camera_Module" target="_blank">Embedded Linux Wiki</a>, the Pi NoIR camera has a CMOS <a href="http://www.ovt.com/products/sensor.php?id=66" target="_blank">Omnivision 5647 CMOS</a> chip. Also see the pdf <a href="http://www.ovt.com/download_document.php?type=sensor&amp;sensorid=66" target="_blank">spec/ad sheet</a>. <a href="http://www.aphesa.com" target="_blank">Aphesa</a> has some pretty in depth discussion of the <a href="http://www.google.com/url?sa=t&amp;rct=j&amp;q=&amp;esrc=s&amp;source=web&amp;cd=3&amp;ved=0CDoQFjAC&amp;url=http%3A%2F%2Fwww.aphesa.com%2Fdownloads%2Fdownload2.php%3Fid%3D1&amp;ei=6DX-UryPKMXb0wGq4YHgBg&amp;usg=AFQjCNG9S8Vix59mZKa5fYeZ-mvSw0ZaOQ&amp;sig2=eRzJXiMlOerKKYQ4RmtkKA&amp;bvm=bv.61190604,d.dmQ" target="_blank">spectral response properties of silicon image sensors</a>.

I tried 950nm LEDs and got a pretty grainy video, I switched to 850 nm LEDs and the image is brighter and less grainy (as expected). In both these cases, the camera is about 20" from subject and IR  lights are off to the left and right, 4 LEDs on the left and 4 LEDs on the right. See <a href="http://www.raspberrypi.org/forum/viewtopic.php?f=43&amp;t=60103" target="_blank">this</a> discussion and <a href="http://www.raspberrypi.org/phpBB3/viewtopic.php?f=43&amp;t=48787" target="_blank">here</a> for a guess at the spectral sensitivity.

<del><span style="font-size: 1rem; line-height: 1.714285714;">-Try -night switch for video with IR LEDs.</span></del>

<span style="line-height: 1.714285714; font-size: 1rem;">-</span><a style="line-height: 1.714285714; font-size: 1rem;" href="http://www.lukasz-skalski.com/category/software/" target="_blank">Raspberry Control</a><span style="line-height: 1.714285714; font-size: 1rem;">, a general purpose Android based Raspberry Pi Controller.</span>

<span style="line-height: 1.714285714; font-size: 1rem;"> Camera board has 2mm screw holes, see </span><a style="line-height: 1.714285714; font-size: 1rem;" href="http://www.scribd.com/doc/142718448/Raspberry-Pi-Camera-Mechanical-Data" target="_blank">Gert's drawings</a><span style="line-height: 1.714285714; font-size: 1rem;">.</span>

&nbsp;

&nbsp;
