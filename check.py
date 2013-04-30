# -*- coding: utf-8 -*-
import mongo
from get_coin import difficulty
from hashlib import sha512
import command


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


class Check(command.Command):
    """ TBD (to be documented) """
    required = ['winning_string', 'winning_hash', 'addr']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        if not mongo.db.addresses.find_one({"addr": addr}):
            self.error("Your address does not exist")
            return

        winning_string = self.data['winning_string']
        winning_hash = self.data['winning_hash']

        is_same_hash = winning_hash == sha512(winning_string).hexdigest()
        coin_exists = mongo.db.coins.find_one({"hash": winning_hash})
        correct_diff = winning_hash.startswith(difficulty() * "0")
        if is_same_hash and not coin_exists and correct_diff:
            mongo.db.coins.insert({"hash": winning_hash, "addr": addr})
            self.success({"hash": winning_hash})
        else:
            # Intentionally a bit vague, just so it's not infinitely easy
            self.error("Something went wrong")
