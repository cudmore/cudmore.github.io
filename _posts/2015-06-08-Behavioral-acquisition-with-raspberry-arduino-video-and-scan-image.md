---
layout: post
title: "Behavioral data acquisition with Raspberry, Arduino, Video and ScanImage"
category: post
date: 2015-06-08 22:01:06
tags:
- linux
- raspberry pi
- ScanImage
- data acquisition
---

Have a Raspberry Pi be the master control for a trial based experiment. Each trial is started by the Pi, the Pi triggers an Arduino and ScanImage (via TTL) and then saves Arduino based timestamped events to a file while recording real-time timestamped video.

See github code and full documentation at [https://github.com/cudmore/triggerserver](https://github.com/cudmore/triggerserver).

