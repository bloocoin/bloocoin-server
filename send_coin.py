# -*- coding: utf-8 -*-
import mongo
import command


class SendCoin(command.Command):
    """ Allows users to move coins from their address
        to another users, given they have enough coins
        for the transaction.
        This requires the ADDR and PWD from the bloostamp,
        which is the same as the ones sent to register.

        fingerprint: {"cmd": "send_coin", "to": _, "addr": _, "pwd": _}
    """
    required = ['amount', 'to', 'addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        to = self.data['to']
        pwd = self.data['pwd']
        valid_account = mongo.db.addresses.find_one({"addr": addr, "pwd": pwd})
        valid_recipient = mongo.db.addresses.find_one({"addr": to})
        if not valid_account:
            self.error("Your address or password was invalid")
            return
        if not valid_recipient:
            self.error("The given recipient does not exist")
            return

        amount = self.data['amount']
        if amount <= 0:
            self.error("Amount must be one or more")
            return
        coins = mongo.db.coins.find({"addr": addr}).count()
        if coins < amount:
            self.error("You don't have enough coins")
            return
        for _ in xrange(0, amount):
            before = mongo.db.coins.find_one({"addr": addr})
            before['addr'] = to
            mongo.db.coins.update({"addr": addr}, before)
        mongo.db.transactions.insert({
            "to": to,
            "from": addr,
            "amount": amount
        })
        self.success({"to": to, "from": addr, "amount": amount})
