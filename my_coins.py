# -*- coding: utf-8 -*-
import mongo
import command


class MyCoins(command.Command):
    """ TBD (to be documented) """
    required = ['addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        pwd = self.data['pwd']
        if mongo.db.address.find_one({"addr": addr, "pwd": pwd}):
            coins = len(mongo.db.coins.find({"addr": addr}))
            self.success({"amount": coins})
            return
        else:
            self.error("Your address or password was invalid")
