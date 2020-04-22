from sql_interactions import *

def capture_id(uid, id):
    add_mountain_to_user(uid,id)
    

def capture_zip(lat,lng):
    uid = get_new_uid(lat,lng)
    f = open("uid.txt", "w")
    f.write(str(uid))
    

def get_uid():
    f = open("uid.txt", "r")
    uid = f.read()
    return uid

def get_weather_info(uid):
    data = get_mountains_hourly(uid, True)
    f = open("weather.txt", "w")
    f.write(str(data))
    return data


