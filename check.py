# -*- coding: utf-8 -*-
import mongo
from get_coin import difficulty
from hashlib import sha512


def check(obj, data):
    """
    {
        "cmd": "check",
        "winning_string": <string>,
        "winning_hash": <hash_of_string>,
        "addr": <address_to_reward>
    }
    """
    try:
        winstr = str(data['winning_string'])
        winhash = str(data['winning_hash'])
        addr = str(data['addr'])
    except KeyError:
        obj.send("False")
        obj.close()
        return

    if not mongo.db.addresses.find_one({"addr": addr}):
        obj.send("False")
        obj.close()
        return

    is_same_hash = winhash == sha512(winstr).hexdigest()
    coin_exists = mongo.db.coins.find_one({"hash": winhash})
    correct_diff = winhash.startswith(difficulty() * "0")
    address_exists = mongo.db.addresses.find_one({"addr": addr})
    if is_same_hash and not coin_exists and correct_diff and address_exists:
        obj.send("True")
        mongo.db.coins.insert({"hash": winhash, "addr": addr})
    else:
        obj.send("False")
    obj.close()
    return
