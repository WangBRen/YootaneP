# -*- coding: utf-8 -*-
import pymongo
import sys
import traceback

MONGODB_CONFIG = {
    'host': 'dds-m5e5d8264bab0fb41671-pub.mongodb.rds.aliyuncs.com',
    'port': 3717,
    'db_name': 'hiq',
    'username': "wbr",
    'password': "666666",
}

class MongoConn(object):

    def __init__(self):
        # connect db
        try:
            self.conn = pymongo.MongoClient(MONGODB_CONFIG['host'], MONGODB_CONFIG['port'])
            self.db = self.conn[MONGODB_CONFIG['db_name']]  # connect db
            self.username=MONGODB_CONFIG['username']
            self.password=MONGODB_CONFIG['password']
            if self.username and self.password:
                self.connected = self.db.authenticate(self.username, self.password)
            else:
                self.connected = True
        except Exception:
            print(traceback.format_exc())
            print('Connect Statics Database Fail.')
            sys.exit(1)