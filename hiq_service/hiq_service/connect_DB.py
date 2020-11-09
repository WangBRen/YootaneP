# -*- coding: utf-8 -*-
import os
import pymysql

MYSQL_ADDRESS = os.environ.get('MYSQL_ADDRESS', '')
MYSQL_DB_NAME = os.environ.get('MYSQL_DB_NAME', '')
MYSQL_USER = os.environ.get('MYSQL_USER', '')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')


def connect():
    db = pymysql.connect(MYSQL_ADDRESS, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME, charset='utf8')
    return db
