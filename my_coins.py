# -*- coding: utf-8 -*-
import mongo
import command


def my_coins(obj, data):
    try:
        addr = str(data[u'addr'])
        pwd = str(data[u'pwd'])
    except KeyError:
        obj.send("Error")
        obj.close()
        return
    if mongo.db.addresses.find_one({"addr": addr, "pwd": pwd}):
        # I <3 python.
        coins = len(mongo.db.coins.find({"addr": addr}))
        obj.send(str(coins))
        obj.close()
    else:
        obj.send("Key Error")
    return


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
