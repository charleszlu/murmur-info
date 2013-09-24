# Munin-Plugins
Several plugins for [MUNIN](http://munin-monitoring.org/).

## minecraft_
Description: Shows user count and RAM usage.
Website: http://wiki.natenom.name/minecraft/munin-plugin

### Installation
As the script needs root rights to work correctly, you must add following
two lines to /etc/munin/plugin-conf.d/munin-node on Debian:
  [minecraft_*]
  user root

If your server is running on the default port, do as root (or with sudo):
```
  cd /etc/munin/plugins
  ln -s /path/to/minecraft_ minecraft_25565
```

## murmur-munin.py
Munin plugin to query a Mumble-Server (Murmur).

[Project Page (German)](http://wiki.natenom.name/mumble/tools/munin)

### Features
* Support to set [messagesizemax](http://wiki.natenom.name/mumble/benutzerhandbuch/murmur/messagesizemax) value.

