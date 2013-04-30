# -*- coding: utf-8 -*-
import json


class Command(object):
    def __init__(self, sock, data):
        self.sock = sock
        try:
            self.data = json.loads(data)
        except ValueError:
            self.error("Unable to decode request JSON")
            return

    def handle(self, *args, **kwargs):
        self.error("This command has not been implemented correctly")

    def success(self, payload, message=None, close=True):
        self.sock.send(json.dumps({
            "success": True,
            "message": message,
            "payload": payload
        }))
        if close:
            self.sock.close()

    def error(self, message, payload=None, close=True):
        self.sock.send(json.dumps({
            "success": False,
            "message": message,
            "payload": payload
        }))
        if close:
            self.sock.close()
