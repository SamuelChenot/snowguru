import subprocess
import struct
from sys import version_info

#create guest variable
is_guest = False

#create the initial user data
def initial_data():
    user_data["zip"] = input("Zip Code: ").lower()
    print(user_data)

    return user_data

#write user data to a json file
def write_data(user_data):
    pass

#get the information from the data file for various uses
def get_data():
    pass

#Access settings to be able to view and alter user data
def settings():
    #specify user data that needs to go into this file
    user_data = get_data()
    try:
        for key in user_data:
            print (key, 'corresponds to', user_data[key])
        write_data(user_data)
    except IndexError:
        user_data = {}
    return user_data
