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


cmds = {

            "get_coin":get_coin.get_coin, #
            "register":register.register,  #         #Commands of the BlooCoin protocol
            "send_coin":send_coin.send_coin,
            "my_coins":my_coins.my_coins, #
            "check":check.check,
            "transactions":transactions.transactions, #
        }

def main():
    port = 3122
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', port))

    sock.listen(5)
    while True:
        obj, conn = sock.accept()
        try:
            data = obj.recv(1024)
        except:
            obj.close()   #This will only happen if the client suddenly disconnects as it is making a request.
            continue
        print conn[0], data
        if data:
            threading.Thread(target=handle, args=(data, obj)).start() #If data we start some need to then parse the data in json format.
        else:
            continue

def handle(data, obj): #Function for parsing commands, {'cmd':command}
    try:
        data = json.loads(data)
        cmds[data[u'cmd']](obj, data)
    except Exception, error:                     #If data is not in the json format it will log the error.
        print error
        return
        #with open("log.txt", 'a') as file:
            #file.write(error)


if __name__ == "__main__":
    main()


        


