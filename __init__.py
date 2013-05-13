# -*- coding: utf-8 -*-
__version__ = "1.2.0-stable"
# X.Y.Z-<branch>

import socket
import get_coin
import send_coin
import my_coins
import check
import transactions
import time
import threading
import register
import json
import total_coins

# Note: When adding new commands, increment the Y of the
# __version__ above.
ncmds = {
    "get_coin": get_coin.GetCoin,
    "register": register.Register,
    "send_coin": send_coin.SendCoin,
    "my_coins": my_coins.MyCoins,
    "check": check.Check,
    "transactions": transactions.Transactions,
    "total_coins": total_coins.TotalCoins,
}


def main():
    port = 3122
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))

    sock.listen(5)
    while True:
        obj, conn = sock.accept()
        threading.Thread(target=handle, args=(obj,conn)).start()


def handle(obj, conn):  # Function for parsing commands, {'cmd':command}
    try:
        data = obj.recv(1024)
    except:
        obj.close()
        return
    if not data:
        return
    print conn[0], str(data)
    try:
        d = json.loads(data)
        cmd = ncmds[d['cmd']](obj, data)
        if cmd._handle:
            cmd.handle()
    except ValueError as e:
        # If there's a decoding error, send them a reply,
        # so they're not just left hanging.
        obj.send(json.dumps({
            "success": False,
            "message": "Unable to parse JSON request",
            "payload": {
                "request": data
            }
        }))
    except Exception as e:
        # If data is not in the json format it will log the error.
        print e

if __name__ == "__main__":
    main()
