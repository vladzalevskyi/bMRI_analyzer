#!/usr/bin/env python
# -*- coding: utf-8 -*-

############################################################
#                                                          #
# Simple script to connect to a remote mysql database      #
#                                                          #
#                                                          #
# Install MySQLdb package by running:                      #
#                                                          #
#                       pip install MySQL-python           #
#                                                          #
############################################################
"""

import MySQLdb as db

HOST = "http://10.35.2.26/"
PORT = 33319
USER = "ka7605"
PASSWORD = "123456"
DB = "coursework_db"

try:
    connection = db.Connection(host=HOST, port=PORT,
                               user=USER, passwd=PASSWORD, db=DB)

    dbhandler = connection.cursor()
    dbhandler.execute("SELECT * from your_table")
    result = dbhandler.fetchall()
    for item in result:
        print (item)

except Exception as e:
    print (e)

finally:
    connection.close()
"""

import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(host='zanner.org.ua', database='coursework_db',user='ka7605', password='123456', port=33321)
  print("Successfully connected!")
  cursor = cnx.cursor()
  query = ("SELECT * FROM images")
  cursor.execute(query)
  print(cursor.fetchall())
  cursor.close()
  cnx.close()
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
"""
import mysql.connector
cnx = mysql.connector.connect(host='zanner.org.ua', database='coursework_db',user='ka7605', password='123456', port=33319)
cursor = cnx.cursor()
query = "SELECT * FROM images;"
cursor.execute(query)
print(query)

cursor.close()
cnx.close()"""