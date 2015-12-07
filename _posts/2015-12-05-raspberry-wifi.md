---
layout: post
title: "Raspberry Wifi"
category: post
date: 2015-12-05 22:01:06
tags:
- debian
- linux
- raspberry
---

Yet another blog post on getting the Raspberry Pi up on a wifi network.

###Configure /etc/network/interfaces

The stock install of Raspian should already have this.

```
sudo pico /etc/network/interfaces
```

```
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

###Edit wpa_supplicant.conf

```
sudo pico /etc/wpa_supplicant/wpa_supplicant.conf 
```

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETGEAR28"
    psk="your_password_here"
}
```

###Tell your router to assign an ip based on MAC address of wifi adapter

```
ifconfig wlan0
```

The MAC address is listed as 'HWaddr' and in this case is '00:0b:81:89:11:8a'.

```
wlan0     Link encap:Ethernet  HWaddr 00:0b:81:89:11:8a  
          inet addr:192.168.1.12  Bcast:192.168.1.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1112 errors:0 dropped:837 overruns:0 frame:0
          TX packets:348 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:253265 (247.3 KiB)  TX bytes:56154 (54.8 KiB)
```

###Change the default name of your Pi in Apple-File-Protocol (e.g. Netatalk) 

```
#stop netatalk
sudo /etc/init.d/netatalk stop

#edit config file
sudo nano /etc/netatalk/AppleVolumes.default

#change this one line

# By default all users have access to their home directories.
#~/                     "Home Directory"
~/                      "pi50"

#restart netatalk
sudo /etc/init.d/netatalk start
```

###Startup mailer

Purpose here is to have your Pi email you when it gets a network connection. This is very useful (and necessary) if the IP is changing with automatic DHCP.

This is startup_mailer.py (in all its crappy code style)

```
import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText
import datetime
import sys

eventText = ''
if len( sys.argv ) > 1:
    eventText = sys.argv[1]
# Change to your own account information
to = 'robert.cudmore@gmail.com'
gmail_user = 'cudmore.raspberry'
gmail_password = 'your_password_here'
smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)

#a linux command line call
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()

ipaddr = split_data[split_data.index('src')+1]
routerAddress = split_data[split_data.index('via')+1]

#eventText is parameter to this function
mail_body = 'raspberrycam2 %s:\n' % eventText
mail_body += 'IP: %s\n' % ipaddr
mail_body += 'router: %s' % routerAddress

today = datetime.date.today()
timeStr = today.strftime('%b %d %Y')

mail_subject = 'pi50 booted at ip ' + ipaddr + ' ' + eventText + ' on %s' % time
Str

msg = MIMEText(mail_body)
msg['Subject'] = mail_subject
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
```

###Another version of my startup_mailer.py

```
import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText
from datetime import datetime, date, time

# Change to your own account information
to = 'robert.cudmore@gmail.com'
gmail_user = 'cudmore.raspberry@gmail.com'
gmail_password = 'your_password_here'
smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)

dt=datetime.now()  

# Very Linux Specific
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]
mail_body = 'raspberrycam2 booted with IP: %s' %  ipaddr
msg = MIMEText(mail_body)
msg['Subject'] = 'raspberrycam2 @ '+ipaddr+' BOOT on %s' % dt.strftime('%b %d %Y, %H:%M:%S')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
```

###Edit /etc/rc.local 

rc.local will run code each itme a user logs in.

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
  python /home/pi/code/startup_mailer.py
fi

exit 0
```

###Useful network commands

```
#scan for available wifi networks
sudo iwlist wlan0 scan
#show network adapter status
ifconfig wlan0
#turn off and on network adapter
sudo ifdown wlan0
sudo ifup wlan0
```

