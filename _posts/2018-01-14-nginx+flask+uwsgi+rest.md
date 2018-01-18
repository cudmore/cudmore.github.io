---
layout: post
title: "nginx+flask+uwsgi+rest"
category: post
date: 2018-01-14 01:01:06
tags:
- nginx
- linux
---

- Run an nginx web server
- Route mmclient to mmclient/index.html
- Run Flask REST app as a service inside uwsgi


## Restart nginx

	sudo systemctl restart nginx
	
## start `myproject.service`

	sudo systemctl start myproject.service
	sudo systemctl stop myproject.service
	sudo systemctl restart myproject.service
	sudo systemctl status -l myproject.service

	sudo systemctl start mmserver.service
	sudo systemctl stop mmserver.service
	sudo systemctl restart mmserver.service
	sudo systemctl status -l mmserver.service

sudo usermod -aG www-data cudmore

sudo chown -R cudmore:www-data /home/cudmore/PyMapManager/*

sudo ln -s /etc/nginx/sites-available/mmserver /etc/nginx/sites-enabled

### Move mmclient/ into /var/www/html/

	sudo cp -R ~/PyMapManager/mmclient/ /var/www/html/
	
Now I can browse

	http://192.168.1.200/mmclient

Run uWSGI manually

	cd /home/cudmore/mmserver
	source venv/bin/activate
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w mywsgi:app

When i change mmserver.py, restart service

	sudo systemctl restart mmserver.service
	sudo systemctl status -l mmserver.service


## Contents of `/home/cudmore/myproject/myproject.py`

```
from flask import Flask
application = Flask(__name__)

@application.errorhandler(404)
def page_not_found(e):
    # your processing here
    return 'NOT FOUND XXX'

@application.route("/api/")
def api():
    return "<H1>API !!!</H1>"

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
```


## Contents of /home/cudmore/myproject/mywsgi.py

```
from myproject import application

if __name__ == "__main__":
    application.run()
```


## Contents of /home/cudmore/myproject/myproject.ini

```
[uwsgi]
module = mywsgi

master = true
processes = 5

socket = myproject.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

## Contents of /etc/systemd/system/myproject.service

```
[Unit]
Description=uWSGI instance to serve mmserver
After=network.target

[Service]
User=cudmore
Group=www-data
WorkingDirectory=/home/cudmore/myproject
Environment="PATH=/home/cudmore/myproject/venv/bin"
ExecStart=/home/cudmore/myproject/venv/bin/uwsgi --ini myproject.ini

[Install]
WantedBy=multi-user.target
```

## Contents of /etc/nginx/sites-available/myproject

Change this to `/etc/nginx/sites-available/mmserver`

Need to change `cudmore` user group

	sudo usermod -aG www-data cudmore
	
Need to link this file into default nginx configuration

	ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
	
```
server {
    listen 80;
    server_name 192.168.1.200;

    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # not working
    location /mmclient {
        root /home/cudmore/PyMapManager/mmclient;
        #root /var/www/html/testclient;
        try_files $uri $uri/ /index.html;
    }

    location /api/v2 {
        include uwsgi_params;
        #uwsgi_pass unix:/home/cudmore/myproject/myproject.sock;
        uwsgi_pass unix:///home/cudmore/mmserver/mmserver.sock;
    }
}
```

