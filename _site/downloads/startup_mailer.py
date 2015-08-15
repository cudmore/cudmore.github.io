import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText
import datetime
import sys
from time import strftime

eventText = ''
if len( sys.argv ) > 1:
    eventText = sys.argv[1]
# Change to your own account information
to = 'robert.cudmore@gmail.com'
gmail_user = 'cudmore.raspberry@gmail.com'
gmail_password = 'ENTER_YOUR_PASSWORD_HERE'
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
mail_body = 'raspberrycam1 %s:\n' % eventText
mail_body += 'IP: %s\n' % ipaddr
mail_body += 'router: %s' % routerAddress

timeStr = strftime('%b %d %Y, %H:%M:%S')

mail_subject = 'raspberrycam1 pi@' + ipaddr + ' ' + eventText + ' on %s' % timeStr

msg = MIMEText(mail_body)
msg['Subject'] = mail_subject
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
