# -*- coding: utf-8 -*-
import json

import mongo
import command


def register(obj, data):
    try:
        addr = str(data[u'addr'])  # Don't want them in unicode
        pwd = str(data[u'pwd'])
    except KeyError:
        obj.close()
        return
    if len(addr) != 40:  # SHA-1 hash is 40 characters
        obj.send("Registration Failed")
        obj.close()
        return

    if not mongo.db.addresses.find_one({"addr": addr}):
        mongo.db.addresses.insert({"addr": addr, "pwd": pwd})
        obj.send("True")
    else:
        obj.send("Your account is already registered.")
    obj.close()
    return


class Register(command.Command):
    """ TBD (to be documented) """
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
