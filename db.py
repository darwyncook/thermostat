__author__ = 'cook'
import mysql.connector
from mysql.connector import errorcode


## The database should have places for:
##    probe # - which is a string
##    zone - string
##    date - datetime
##    time - datetime
##    temperature in F - Number
##    temperature in C - Number

class db:
    config = {'user': 'monitor', 'password': 'Pi314159', 'host': 'localhost', 'database': 'temps',
          'raise_on_warnings': True}
    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password for the temperature database")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Temperature database does not exists")
            else:
                print(err)