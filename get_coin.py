# -*- coding: utf-8 -*-
import json
import random

import mongo
import command


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


class GetCoin(command.Command):
    """ Allows clients to request the server difficulty.
        Previously also gave a starting point, but this was
        removed, as it was useless (as shown in blc-hash).
        Only used by miners atm.

        When real cryptography is added, this will give the
        current coin to the miner so they can all work towards
        the same coin.
    """
    def handle(self, *args, **kwargs):
        self.success({"difficulty": difficulty()})
