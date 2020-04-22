from uszipcode import SearchEngine

#declare a basic global search variable
search = SearchEngine(simple_zipcode=True)

def zip_to_city_state(zipcode):
    city_state = search.by_zipcode(zipcode).to_dict()
    #print("dict: ", city_state)

    city = city_state["major_city"]
    state = city_state["state"]
    #print("city: ", city, " state: ", state)

    return city, state

def zip_to_coords(zipcode):
    zip_dict = search.by_zipcode(zipcode).to_dict()

    latitude = zip_dict["lat"]
    longitude = zip_dict["lng"]
    
    return latitude, longitude