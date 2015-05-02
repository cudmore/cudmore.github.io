---
layout: post
title: "Python tricks"
category: post
date: 2015-04-30 22:01:06
tags:
- python
---

####iPython auto reload imports

    %load_ext autoreload
    %autoreload 2

To autoload these options, see:

http://stackoverflow.com/questions/1907993/autoreload-of-modules-in-ipython/10472712#10472712

    ipython profile create
    
    c.InteractiveShellApp.exec_lines = []
    c.InteractiveShellApp.exec_lines.append('%load_ext autoreload')
    c.InteractiveShellApp.exec_lines.append('%autoreload 2')


