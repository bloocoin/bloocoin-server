# -*- coding: utf-8 -*-
import json

import mongo
import command


class Transactions(command.Command):
    """ TBD (to be documented) """
    required = ['addr', 'pwd']

    def handle(self, *args, **kwargs):
        addr = self.data['addr']
        pwd = self.data['pwd']
        if not mongo.db.addresses.find_one({"addr": addr, "pwd": pwd}):
            self.error("Your address or password was invalid")
            return
        payload = {"transactions": []}
        for t in mongo.db.transactions.find({"to": addr}):
            payload['transactions'].append({
                "from": t['from'],
                "to": addr,
                "amount": t['amount']
            })
        for t in mongo.db.transactions.find({"from": addr}):
            payload['transactions'].append({
                "from": addr,
                "to": t['to'],
                "amount": x['amount']
            })
        self.success(payload)
