# -*- coding: utf-8 -*-
import json

import mongo
import command


class Register(command.Command):
    """ Allows clients to register their address with the
        server's central database. If a given address
        already exists, they should regenerate and try
        again with a new one, if the user requested a
        registration.

        fingerprint: {"cmd": "register", "addr": _, "pwd": _}
    """
    required = ['addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        pwd = self.data['pwd']
        if len(addr) != 40:
            self.error("Registration unsuccessful")
            return
        if mongo.db.addresses.find_one({"addr": addr}):
            self.error("That address already exists")
            return
        mongo.db.addresses.insert({"addr": addr, "pwd": pwd})
        self.success({"addr": addr})
