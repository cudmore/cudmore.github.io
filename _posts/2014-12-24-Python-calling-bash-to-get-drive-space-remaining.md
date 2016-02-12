---
layout: post
title: Python calling bash to get drive space remaining
tags:
- python
---

I need to have some Python code tell me how much drive space is left. Here is what I came up with.

~~~
>>> import subprocess as sub
>>> checkPath = '~/video'
>>> cmd = "df " + checkPath + " | awk '{ print $5 }' | tail -n 1"
>>> p = sub.Popen(cmd, stdout=sub.PIPE,stderr=sub.PIPE, shell=True)
>>> (out, err) = p.communicate()
>>> out
'31%\n'
>>> out.rstrip() # rstrip 'chomps' off newline
'31%'
~~~
