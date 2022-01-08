from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import secrets
import requests
import json

debug = False

def debugPrint(message):
    if debug == True:
        print(message)

def GetLatLong(locationString):
    geolocator = Nominatim(user_agent="geoapiExercises")
    debugPrint("Location Address:" + locationString)
    location = geolocator.geocode(locationString)
    debugPrint("Long,Lat:" + str(location.latitude) + " " + str(location.longitude))
    return [location.latitude, location.longitude]

def GetTime(latitude, longitude):
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=latitude, lng=longitude)
    debugPrint("Timezone:" + str(result))
    IST = pytz.timezone(result)
    debugPrint("Current Time:" + str(datetime.now(IST)))
    return datetime.now(IST)

def GetWeather(latitude, longitude, detailed):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={secrets.WEATHER_API}"
    response = requests.get(url)
    data = json.loads(response.text)
    returnData = []
    for detail in data["weather"]:
        returnData.append(detail["description"])
    if detailed == True:
        for detail in data["main"]:
            returnData.append(detail["temp"])
        for detail in data["wind"]:
            returnData.append(detail["speed"], detail["deg"])
        for detail in data["sys"]:
            returnData.append(detail["sunrise"], detail["sunset"])
    debugPrint(returnData)
    return returnData

def TimeAndWeather(locationString, detailed):
    locLatLong = GetLatLong(locationString)
    locTime = GetTime(locLatLong[0], locLatLong[1])
    locWeather = GetWeather(locLatLong[0], locLatLong[1], detailed)
    return locTime, locWeather

locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "India"]
for location in locations:
    locTimeWeather = TimeAndWeather(location, True)
    print(location)
    print(locTimeWeather[0])
    print(locTimeWeather[1])
    print("")