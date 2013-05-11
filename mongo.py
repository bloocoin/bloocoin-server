# -*- coding: utf-8 -*-
import pymongo

#Only change for remote authentication
host = "localhost"
port = 27017
username = ""
password = ""

db = pymongo.MongoClient(host, port).bloocoin
db.authenticate(username, password)
