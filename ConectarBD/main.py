# Importing module 
#import mysql.connector
  
# Creating connection object
#mydb = mysql.connector.connect(
 #   host = "localhost",
  #  user = "root",
   # password = "hipotenusa00"
#)
  
# Printing the connection object 
#print(mydb)

import json
import pymysql

connection = pymysql.connect(user = "root", password = "hipotenusa00", host = "localhost", port = 3306)
with connection.cursor(pymysql.cursors.DictCursor) as cursor:
    cursor.execute("SELECT * FROM world.city")
    rows = cursor.fetchall()
    for row in rows:
       print(row.values())