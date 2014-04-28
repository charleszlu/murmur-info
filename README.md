# Munin-Plugins
Several plugins for [MUNIN](http://munin-monitoring.org/).

## minecraft_
Description: Shows user count and RAM usage.

[Project page (German)](http://wiki.natenom.name/minecraft/munin-plugin)

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
A MUNIN plugin to query a Mumble-Server (Murmur).

Available data:
* users (all)
* users (not authenticated)
* server uptime in days
* ban count

Documentation (English): http://w.natenom.name/wiki/Munin_plugin_for_a_Murmur_%28Mumble-Server%29
Documentation (German): http://wiki.natenom.name/mumble/tools/munin

### Features
* Support to set [messagesizemax](http://wiki.natenom.name/mumble/benutzerhandbuch/murmur/messagesizemax) value.

