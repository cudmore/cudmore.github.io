---
layout: post
title: "Auto login to ssh servers"
category: post
date: 2015-05-04 22:01:06
tags:
- linux
---

In order to automatically login to an ssh server, you need to generate public/private rsa key pairs on a client and copy these keys to an ssh server. Next time you login from the client to the server, you won’t need to enter your password.

You should learn and understand a bit about ssh and its security implementations, mostly rsa. Your privacy is only as good as your ability to keep your keys secret, here is a recent example of a nifty ‘side channel attack‘ to obtain your secret keys.

In what follows I am setting up automatic rsa authentication from a client to a server:

- client: OS X or Linux, cudmore$
- server: Raspian, pi@192.168.1.70

#### [Client] Generate public/private rsa key pair

    ssh-keygen -t rsa

	Generating public/private rsa key pair.
	Enter file in which to save the key (/Users/cudmore/.ssh/id_rsa): 
	/Users/cudmore/.ssh/id_rsa already exists.
	Overwrite (y/n)? y
	Enter passphrase (empty for no passphrase): 
	Enter same passphrase again: 
	Your identification has been saved in /Users/cudmore/.ssh/id_rsa.
	Your public key has been saved in /Users/cudmore/.ssh/id_rsa.pub.
	The key fingerprint is:
	a3:73:53:ee:68:54:37:e9:aa:64:68:4d:30:c3:4f:3a cudmore@localhost
	The key's randomart image is:
	+--[ RSA 2048]----+
	|                 |
	|     .           |
	|      = .    .   |
	|       B  . +    |
	|      E S..o .   |
	|       *.+  .    |
	|      =.* ..     |
	|     . =.+.      |
	|       .o..      |
	+-----------------+

#### [Client] id_rsa.pub from the client to the ssh server (need to enter password)

    scp ./.ssh/id_rsa.pub pi@192.168.1.70:~/id_rsa.pub

#### [Client] Login to the ssh server (last time you will need a password)

    ssh pi@192.168.1.70

#### [Server] Copy the key into the correct location (on the server)

    cat id_rsa.pub >> ./.ssh/authorized_keys

#### [Server] Delete the original (on the server)

    rm ./id_rsa.pub

#### [Client] The next time you login you will not be asked for a password

    ssh pi@192.168.1.70

#### Notes

- If your Raspberry does not have a ./.ssh directory you need to turn on ssh using ‘sudo raspi-config’ -> advanced options -> ssh
- When you append to authorized_keys with ‘cat id_rsa.pub >> ./.ssh/authorized_keys’, the file will be created if it does not exist.
- If your client is Mac OS X you will be asked for a passphrase when you generate your ssh public/private keys with ‘ssh-keygen -t rsa’. This is an extra level of security. The first time you login to your ssh server, OS X will ask for this passphrase. Again, your security is only as good as you keeping your passwords safe. Using a passphrase for your OSX keychain is convenient but if someone gets this passphrase, they in turn get all your passwords within your keychain. This may seem very circular and it is, the art is in being creative in breaking the loop.

#### Fun

-ssh -o VisualHostKey=yes pi@192.168.1.70
