---
layout: post
title: Bit Torrent Sync
category: post
date: 2016-01-20 22:01:06
tags:
- debian
- raspberry
---

Once this is done, folders can be synchronized between machines running btsync. This could be done with open source OwnCloud or paid Dropbox but neither of them have a command line (headless) synch tool (as of January 2016) and neither of them will work on a LAN without a central server. This is the power of BitTorrent. An added perk is that I have a legitimate aliby if my ISP ever accuses me of pirating over the bittorrent network.

Benefits

  - Neither OwnCloud or Dropbox have headless sync clients (as of January 2016)
  - There is no limit on drive space
  - btsync can work on a lan with no internet
  - btsync should be faster

See bittorrent sync

https://www.getsync.com

###Install bittorrent sync

####Download
```
#debian
wget https://download-cdn.getsync.com/stable/linux-x64/BitTorrent-Sync_x64.tar.gz
tar -zxvf BitTorrent-Sync_x64.tar.gz

#raspberry/arm
wget https://download-cdn.getsync.com/stable/linux-arm/BitTorrent-Sync_arm.tar.gz
```

####install and run by hand

```
#by default runs on localhost:8888, run as external ip (external meaning on my LAN)
./btsync  --webui.listen 192.168.1.200:8888

#kill daemon
pkill btsync
```

####Making btsync run at boot (raspbian)

Add the following to /etc/rc.local

```
/home/pi/btsynch/btsync --webui.listen 192.168.1.60:8888
```

####Making btsync run at boot (debian)

Way more complicated than Rasbian, but, following this perfect github gist:

https://gist.github.com/MendelGusmao/5398362

Once all of this is done you can interact with the btsync daemon:

```
sudo /etc/init.d/btsync start
sudo /etc/init.d/btsync stop
sudo /etc/init.d/btsync status
```

And configure your shares from a browser

```
http://192.168.1.200:8888
```

####Move btsync binary into place

```
sudo cp ./btsync /usr/bin/
```

####Modify btsync daemon script

Careful here, different from btsync binary but SAME name

```
sudo mv btsync /etc/init.d/
sudo chmod +x /etc/init.d/btsync
```

At this point I thought I could run the daemon without specifying a ~/.sync/config.json file but this does NOT work because the daemon will run inside /etc/init.d/ and try to create a .sync/ but it is not allowed to.

####Make a ~/.sync folder in your user directory

This is my ~/.sync/config.json. Shared_folders will be specified in web ui. Changes from original gist include:

  - "device_name": "debian",
  - "storage_path": "/home/cudmore/.sync",
  - "listen": "192.168.1.200:8888",

```
{
  "device_name": "debian",
  "listening_port": 0,
  "storage_path": "/home/cudmore/.sync",
  "check_for_updates": true, 
  "use_upnp": true,
  "download_limit": 0,                       
  "upload_limit": 0, 
  "webui": {
    "listen": "192.168.1.200:8888",
    "login" : "admin",
    "password" : "password"
  },
  "shared_folders": []
}
```

This is my modified /etc/init.d/btsync daemon script. Well, not really modified except for changing BTSYNC_USER.

```
#!/bin/sh
### BEGIN INIT INFO
# Provides: btsync
# Required-Start: $local_fs $remote_fs
# Required-Stop: $local_fs $remote_fs
# Should-Start: $network
# Should-Stop: $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Multi-user daemonized version of btsync.
# Description: Starts the btsync daemon for all registered users.
### END INIT INFO

# Replace with linux users you want to run BTSync clients for
BTSYNC_USERS="cudmore"
DAEMON=/usr/bin/btsync

start() {
  for btsuser in $BTSYNC_USERS; do
    HOMEDIR=`getent passwd $btsuser | cut -d: -f6`
    config=$HOMEDIR/.sync/config.json
    if [ -f $config ]; then
      echo "Starting BTSync for $btsuser"
      start-stop-daemon -b -o -c $btsuser -S -u $btsuser -x $DAEMON -- --config $config
    else
      echo "Couldn't start BTSync for $btsuser (no $config found)"
    fi
  done
}

stop() {
  for btsuser in $BTSYNC_USERS; do
    dbpid=`pgrep -fu $btsuser $DAEMON`
    if [ ! -z "$dbpid" ]; then
      echo "Stopping btsync for $btsuser"
      start-stop-daemon -o -c $btsuser -K -u $btsuser -x $DAEMON
    fi
  done
}

status() {
  for btsuser in $BTSYNC_USERS; do
    dbpid=`pgrep -fu $btsuser $DAEMON`
    if [ -z "$dbpid" ]; then
      echo "btsync for USER $btsuser: not running."
    else
      echo "btsync for USER $btsuser: running (pid $dbpid)"
    fi
  done
}

case "$1" in
 start)
start
;;
stop)
stop
;;
restart|reload|force-reload)
stop
start
;;
status)
status
;;
*)
echo "Usage: /etc/init.d/btsync {start|stop|reload|force-reload|restart|status}"
exit 1
esac

exit 0
```
