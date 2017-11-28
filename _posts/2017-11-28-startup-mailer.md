---
layout: post
title: "Startup mailer on a Raspberry Pi"
category: post
date: 2017-11-28 01:01:06
tags:
- raspberry
- linux
---

Have a Raspberry Pi send an email when it boots.

Before doing this you need to setup a gmail account to send email from. You will need to reduce the security on this account so please do not use your primary gmail account, set up a new one.


Reduce the security on this account

 - upper right of gmail click on 'my account'
 - select 'sign-in & security'
 - in the 'Apps with account access' section, turn on 'Allow less secure apps'
 
 
Make a `startup_mailer.py` python script.

    cd
    mkdir code
    cd code
    pico startup_mailer.py
    
Paste the following into the file

```python
#!/usr/bin/python
import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText
import datetime
import sys
from time import strftime
import platform # to get host name

message = ''
if len( sys.argv ) > 1:
    message = sys.argv[1]

# list of email accounts to send to
to = ['send to email 1', 'send to email 2']

# Change to your own account information to send from
gmail_user = 'your_gmail_account@gmail.com'
gmail_password = 'your_gmail_password'

smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)

# get ip and router address
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()

ipaddr = split_data[split_data.index('src')+1]
routerAddress = split_data[split_data.index('via')+1]

hostName = platform.node()

mail_body = 'name: ' + hostName + '\n'
mail_body += 'IP: %s\n' % ipaddr
mail_body += 'router: %s\n' % routerAddress
mail_body += 'message: ' + message + '\n'

timeStr = strftime('%b %d %Y, %H:%M:%S')

mail_subject = hostName + ' pi@' + ipaddr + ' on %s' % timeStr

msg = MIMEText(mail_body)
msg['Subject'] = mail_subject
msg['From'] = gmail_user
smtpserver.sendmail(gmail_user, to, msg.as_string())
smtpserver.quit()
```

Have the `startup_mailer.py` python script run at boot

    # make it executable
    cd
    chmod +x code/startup_mailer.py 
    
    # edit crontab
    crontab -e
    
Append this line to crontab, 'boot' is a message to send.

    @reboot (sleep 10; /home/pi/code/startup_mailer.py 'boot')

I am using cudmore.raspberry@gmail.com with my normal password