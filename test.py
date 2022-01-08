from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import secrets
import requests
import json

def GetLatLong(locationString):
    geolocator = Nominatim(user_agent="geoapiExercises")
    print("Location Address:", locationString)
    location = geolocator.geocode(locationString)
    print("Long,Lat:", location.latitude, location.longitude)
    return [location.latitude, location.longitude]

def GetTime(latitude, longitude):
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=latitude, lng=longitude)
    print("Timezone:",result)
    IST = pytz.timezone(result)
    print("Current Time:", datetime.now(IST))

def GetWeather(latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={secrets.WEATHER_API}"
    response = requests.get(url)
    data = json.loads(response.text)
    for doc in data["weather"]:
        print(doc['description'])

def TimeAndWeather(locationString):
    locLatLong = GetLatLong(locationString)
    locTime = GetTime(locLatLong[0], locLatLong[1])
    locWeather = GetWeather(locLatLong[0], locLatLong[1])
    return locTime, locWeather

locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "India"]
for location in locations:
    locTimeWeather = TimeAndWeather(location)
    print(locTimeWeather[0], locTimeWeather[1])