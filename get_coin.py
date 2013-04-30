# -*- coding: utf-8 -*-
import json
import random
import mongo


def get_coin(obj, data):
    # Mining function used for getting the difficulty of the hash.
    # recv {"cmd": "get_coin"}
    # send {"difficulty": 7}
    obj.send(json.dumps({"difficulty": difficulty()}))
    obj.close()
    return


def difficulty():
    # This calculates the difficulty with the lowest being 7
    return mongo.db.coins.count() / 205000 + 7
