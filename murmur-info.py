#!/usr/bin/env python
# -*- coding: utf-8
#
# munin-info.py - "murmur stats (User/Bans/Uptime/Channels)" script.
# Copyright (c) 2019, Charles Lu / c4planted@gmail.com
# Adapted from Natenom's murmur-munin.py
# Copyright (c) 2014, Natenom / natenom@natenom.name
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided
# with the distribution.
# * Neither the name of the developer nor the names of its
# contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE. 
import Ice, sys, os

class MurmurIce:

    def __init__(self, murmur_ice_path, murmur_host, murmur_icesecreatread, ice_port=6502, message_size_max=65535, exclude_keywords=[]):

        # Exclude names containing these keywords from being counted as users.
        # Useful for excluding bots 
        self.exclude_keywords=exclude_keywords

        # Path to Slice and Murmur.ice
        Ice.loadSlice(f"--all -I{Ice.getSliceDir()} {murmur_ice_path}")

        props = Ice.createProperties([])
        # MessageSizeMax; increase this value, if you get a MemoryLimitException.
        # Also check this value in murmur.ini of your Mumble-Server.
        # This value is being interpreted in kibiBytes.
        props.setProperty("Ice.MessageSizeMax", str(message_size_max))
        props.setProperty("Ice.ImplicitContext", "Shared")
        props.setProperty("Ice.Default.EncodingVersion", "1.0")  # Murmur 1.2.x uses Ice protocl 1.0 only

        id = Ice.InitializationData()
        id.properties = props

        self.ice = Ice.initialize(id)

        # Ice Password to get read access.
        # If there is no such var in your murmur.ini, this can have any value.
        # You can use the values of icesecret, icesecretread or icesecretwrite in your murmur.ini
        self.ice.getImplicitContext().put("secret", murmur_icesecreatread)

        import Murmur

        try:
            # Murmur host IP/DNS and ice_port should be provided
            self.meta = Murmur.MetaPrx.checkedCast(self.ice.stringToProxy(f'Meta:tcp -h {murmur_host} -p {ice_port}'))
        except (Ice.DNSException, Ice.ConnectionRefusedException):
            print('Connection refused.')
            exit(1)

        try:
            self.server=self.meta.getServer(1)
        except Murmur.InvalidSecretException: 
            print('Given icesecreatread password is wrong.')
            exit(1)

        self.users = 0
        self.excludedusers = 0
        self.usersnotauth = 0

        self._count_users()

    def __del__(self):
        self.ice.destroy()

    def _count_users(self):
        # count users
        self.users = self.server.getUsers()
        # count the number of users to exclude
        # also count not authenticated users (who are not excluded)
        for user in self.users.values():
            for keyword in self.exclude_keywords:
                if str(keyword).lower() in user.name.lower():
                    self.excludedusers += 1
                    break
            else:
                # not excluded
                if user.userid == -1:
                    self.usersnotauth += 1
        
    def get_all_values(self):
        print(f"users: {(len(self.users)-self.excludedusers)}")
        print(f"uptime: {self.meta.getUptime()}")
        print(f"chancount: {(len(self.server.getChannels())-1)}")
        print(f"bancount: {len(self.server.getBans())}")
        print(f"usersnotauth: {self.usersnotauth}")
        print("state: 1")
        print(f'version: {self.meta.getVersion()[0]}.{self.meta.getVersion()[1]}.{self.meta.getVersion()[2]}')

    def get_value(self, key):
        if key == "users":
            print(len(self.users)-self.excludedusers)

        elif key == "uptime":
            print(self.meta.getUptime())

        elif key == "chancount":
            print(len(self.server.getChannels())-1)

        elif key == "bancount":
            print(len(self.server.getBans()))

        elif key == "usersnotauth":
            print(self.usersnotauth)

        elif key == "state":
            print(1)

        elif key == "version":
            print(f'{self.meta.getVersion()[0]}.{self.meta.getVersion()[1]}.{self.meta.getVersion()[2]}')

        elif key == "useronline" and len(sys.argv) == 3:
            for key in self.users.keys():
                if sys.argv[2].lower() == self.users[key].name.lower():
                    print(1)
                    break
            else:
                print(0)
        else:
            self.get_all_values()


if __name__ == "__main__":

    murmur_ice_path = os.getenv('MURMUR_ICE_PATH')
    murmur_host = os.getenv('MURMUR_HOST', '127.0.0.1')
    ice_port = os.getenv('MURMUR_ICE_PORT', 6502)
    murmur_icesecreatread = os.getenv('MURMUR_ICE_SECRET')
    message_size_max = os.getenv('MURMUR_ICE_MSG_SIZE_MAX', 65535)
    exclude_keywords = os.getenv('EXCLUDE_KEYWORDS', '').split(',')

    if not murmur_ice_path:
        raise RuntimeError('MURMUR_ICE_PATH environment variable is not set!')
    if not murmur_icesecreatread:
        raise RuntimeError('MURMUR_ICE_SECRET environment variable is not set!')

    murmur = MurmurIce(
        murmur_ice_path=murmur_ice_path,
        murmur_host=murmur_host, 
        murmur_icesecreatread=murmur_icesecreatread,
        ice_port=ice_port,
        message_size_max=message_size_max,
        exclude_keywords=exclude_keywords
    )

    # Usage
    if sys.argv[1:]:
        if sys.argv[1] == "help":
            print('useronline [name]: Checks if the user with the name provided is online')
            print('users: Number of users online')
            print('usersnotauth: Number of users online (Not authenticated)')
            print('uptime: Uptime in seconds')
            print('chancount: Channel count')
            print('bancount: Bans on server')
            print("state: Mumble server status")
            print("version: Mumble server version")

        else:
            murmur.get_value(sys.argv[1])

    else:
        murmur.get_all_values()
