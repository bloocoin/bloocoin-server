# -*- coding: utf-8 -*-
import mongo


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
