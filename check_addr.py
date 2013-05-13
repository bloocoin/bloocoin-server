# -*- coding: utf-8 -*-
import mongo
import command

class CheckAddr(command.Command):
    """
    
    {"cmd":"check_addr", "addr":"addr"}
    
    """
    required = ['addr']

    def handle(self, *args, **kargs):
        addr = self.data['addr']
        try:
            amount = mongo.db.coins.find({'addr':addr}).count()
            self.success({"addr":addr, "amount":amount})
        except:
            self.error("Error")
            return
