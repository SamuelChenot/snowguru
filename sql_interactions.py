<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
import pandas as pd
import MySQLdb
import pyodbc
import re



def sort_distence_all(UID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    cursor.callproc('searchDistance',[str(UID), "0", ])
    data = cursor.fetchall()

    return data




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
def get_mountains_daily_info(MID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    sql_string = 'SELECT Mountains.Name, Daily.* FROM Daily'
    sql_string += ' INNER JOIN HomeMT ON Daily.MID = HomeMT.MID'
    sql_string += ' INNER JOIN Mountains ON Daily.MID = Mountains.MID'
    sql_string += ' WHERE '+str(MID)+' = Daily.MID'
    sql_string += ' GROUP BY Daily.Day'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple


#Takes User ID and boolean, returns alphabetically
def search_lex(UID, home):

    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    #SQL processing
    if home == True: home_ = '1'
    else: home_ = '0'

    #SQL processing
    cursor.callproc('searchLex',[str(UID), str(home_), ])
    data = cursor.fetchall()

    cursor.close()

    return data


def update_user_coordinates(UID, LAT, LON):

    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    #SQL processing
    cursor.callproc('updateCoordinates',[str(UID), str(LAT), str(LON), ])

    cursor.close()

    print("Updated User: "+str(UID)+" Coordinates"+str(LAT)+", "+str(LON))


# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_mountain_Names():
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    sql_string = 'SELECT Name, Hourly.MID FROM Mountains'
    sql_string += ' INNER JOIN Hourly On Mountains.MID = Hourly.MID'
    sql_string += ' GROUP BY Mountains.Name;'

    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple

# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_user_list(UID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    sql_string = 'SELECT Mountains.Name, Hourly.MID FROM Hourly'
    sql_string += ' INNER JOIN HomeMT ON Hourly.MID = HomeMT.MID'
    sql_string += ' INNER JOIN Mountains ON Hourly.MID = Mountains.MID'
    sql_string += ' WHERE '+str(UID)+' = HomeMT.UID'
    sql_string += ' GROUP BY Hourly.MID;'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
import pandas as pd
import MySQLdb
import pyodbc
import re



def sort_distence_all(UID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    cursor.callproc('searchDistance',[str(UID), "0", ])
    data = cursor.fetchall()

    return data




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
def get_mountains_daily_info(MID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    sql_string = 'SELECT Mountains.Name, Daily.* FROM Daily'
    sql_string += ' INNER JOIN HomeMT ON Daily.MID = HomeMT.MID'
    sql_string += ' INNER JOIN Mountains ON Daily.MID = Mountains.MID'
    sql_string += ' WHERE '+str(MID)+' = Daily.MID'
    sql_string += ' GROUP BY Daily.Day'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple


# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_mountains_hourly_info(MID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    sql_string = 'SELECT Mountains.Name, Hourly.* FROM Hourly'
    sql_string += ' INNER JOIN HomeMT ON Hourly.MID = HomeMT.MID'
    sql_string += ' INNER JOIN Mountains ON Hourly.MID = Mountains.MID'
    sql_string += ' WHERE '+str(MID)+' = Hourly.MID'
    sql_string += ' GROUP BY Hourly.Hour'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple


#Takes User ID and boolean, returns alphabetically
def search_lex(UID, home):

    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    #SQL processing
    if home == True: home_ = '1'
    else: home_ = '0'

    #SQL processing
    cursor.callproc('searchLex',[str(UID), str(home_), ])
    data = cursor.fetchall()

    cursor.close()

    return data


def update_user_coordinates(UID, LAT, LON):

    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    #SQL processing
    cursor.callproc('updateCoordinates',[str(UID), str(LAT), str(LON), ])

    cursor.close()

    print("Updated User: "+str(UID)+" Coordinates"+str(LAT)+", "+str(LON))


# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_mountain_Names():
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()

    sql_string = 'SELECT Name, Hourly.MID FROM Mountains'
    sql_string += ' INNER JOIN Hourly On Mountains.MID = Hourly.MID'
    sql_string += ' GROUP BY Mountains.Name;'

    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple

# Takes UserID as UID and boolean saying weter to return all mountains or user home mountains
def get_user_list(UID):
    db = MySQLdb.connect('localhost', # The Host
                         'BaseUser', # username
                         'password', # password
                         'mydb') # name of the data base
    cursor = db.cursor()


    sql_string = 'SELECT Mountains.Name, Hourly.MID FROM Hourly'
    sql_string += ' INNER JOIN HomeMT ON Hourly.MID = HomeMT.MID'
    sql_string += ' INNER JOIN Mountains ON Hourly.MID = Mountains.MID'
    sql_string += ' WHERE '+str(UID)+' = HomeMT.UID'
    sql_string += ' GROUP BY Hourly.MID;'


    cursor.execute(sql_string)
    data = cursor.fetchall()

    db.commit()
    cursor.close()

    return data #Formated as a 2d tuple
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
