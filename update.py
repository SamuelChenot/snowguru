#import pymysql as sql
import pandas as pd
import MySQLdb
import csv
import pyodbc
from update_v3 import create_csvs as initiate

#---------------------------------------------------------------------------------------------------------------------------------+
#                                                                                                                                 |
#IMPORTANT: run SET SQL_SAFE_UPDATES = 0; to allow updates if in automatic safe mode                                              |
#                                                                                                                                 |
#Assumes that hourly.csv and daily.csv are already created and formatted properly, if not call the commented out function below   |
#                                                                                                                                 |
#Use pip install mysqlclient     ( I did this on macOS but Ubuntu can use sudo apt-get, but not sure for Windows)                 |
#                                                                                                                                 |
#Note:Do not call on full database to test to prevent running out of calls                                                        |
#                                                                                                                                 |
#---------------------------------------------------------------------------------------------------------------------------------+


#To create csv's give valid list of the moutains applicable to DarkySkies API, index starting at 1
#--Calls Dark Ski API--

# initiate("smallMountain.txt")#  <============Creates .csv's

#Credential information
host = 'localhost'
db = 'mydb'
user = 'BaseUser'
password = 'password'

db = MySQLdb.connect(host, # The Host
                     user, # username
                     password, # password
                     db) # name of the data base

#Open the hourly csv and load into SQL
cursor = db.cursor()
file_object  = open("hourly.csv", "r")
csv_reader = csv.reader(file_object, delimiter=',')

#for row in csv_reader:
for row in csv_reader:
  Query1 = "REPLACE INTO `Hourly`"
  Query2 = "Values("+row[0]+","+row[1]+","+row[2]+", "+row[3]+",'"+row[4]+"',"+row[5]+","+row[6]+","+row[7]+","+row[8]+","+row[9]+","+row[10]+","+row[11]+","+row[12]+","+row[13]+"); "
  Query3 = " "
  cursor.execute(Query1+Query2)   
  db.commit()   
cursor.close()

#Sample data to terminal
sql_string = 'SELECT * FROM Hourly'
data = pd.read_sql(sql_string, con=db) 
print(data) 

#Open daily csv and load data
cursor = db.cursor()
file_object  = open("daily.csv", "r")
csv_reader = csv.reader(file_object, delimiter=',')

#for row in csv_reader:
for row in csv_reader:
  Query1 = "REPLACE INTO `Daily`"
  Query2 = "Values("+row[0]+","+row[1]+","+row[2]+", "+row[3]+","+row[4]+","+row[5]+","+row[6]+",'"+row[7]+"',"+row[8]+","+row[9]+","+row[10]+","+row[11]+","+row[12]+","+row[13]+","+row[14]+","+row[15]+","+row[16]+"); "
  Query3 = " "
  cursor.execute(Query1+Query2)   
  db.commit()   
cursor.close()

#Sample data to terminal
sql_string = 'SELECT * FROM Daily'
data = pd.read_sql(sql_string, con=db)
print(data)     
