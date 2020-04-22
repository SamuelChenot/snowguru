import pandas as pd
import MySQLdb
import pyodbc
import re


#Get a unique user ID
def get_new_uid(latitude, longitude):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    #SQL processing
    sql_string = 'SELECT * FROM Clients;'
    data = pd.read_sql(sql_string, con=db)
    cursor.execute('CALL createUser(@newID);')
    sql_string = 'SELECT @newID;'
    cursor.execute(sql_string)
    data = cursor.fetchone()[0]
    db.commit()

    print("UserID: ", data, " created.")
    return int(data)



#Add a mountain to a user ID
def add_mountain_to_user(UID, MID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    #SQL processing
    cursor.callproc('toggleHome',[str(UID), str(MID), ])

    db.commit()
    cursor.close()

    print("Mountain ID: ", MID, "Toggled to UserID: ", UID)

# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_mountains_hourly(UID, home_mountain):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    if home_mountain == False:
        sql_string = 'SELECT * FROM Hourly'

    if home_mountain == True:
        sql_string = 'SELECT * FROM Hourly'
        sql_string += ' INNER JOIN HomeMT ON Hourly.MID = HomeMT.MID'
        sql_string += ' WHERE '+str(UID)+' = HomeMT.UID'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple

