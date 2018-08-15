#!/usr/bin/env python3

#Code is from week 4 lab archive

import sqlite3 as lite
import sys
con = lite.connect('sensehat.db')
with con: 
    cur = con.cursor() 
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_data(timestamp DATETIME, temp NUMERIC, humid NUMERIC, pressure NUMERIC)")
