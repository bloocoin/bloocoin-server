# -*- coding: utf-8 -*-
import json

import mongo
import command


def transactions(obj, data):
    try:
        addr = str(data[u'addr'])
        pwd = str(data[u'pwd'])
    except KeyError:
        obj.send("Error")
        obj.close()
        return
    if mongo.db.addresses.find_one({"addr": addr, "pwd": pwd}):
        for x in mongo.db.transactions.find({"to": addr}):
            obj.send(json.dumps({
                "from": x['from'],
                "to": addr,
                "amount": x['amount']
            })+"\n")
        for x in mongo.db.transactions.find({"from": addr}):
            obj.send(json.dumps({
                "from": addr,
                "to": x['to'],
                "amount": x['amount']
            })+"\n")
        obj.close()
        return


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
