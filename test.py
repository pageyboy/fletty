from flask import Flask
from datetime import datetime
from waitress import serve
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import secrets
import requests
import json
from extract import json_extract

debug = False
locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "India"]

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
    returnData.append(json_extract(data, "description"))
    if detailed == True:
        returnData.append(json_extract(data, "temp"))
        returnData.append(json_extract(data, "speed"))
        returnData.append(json_extract(data, "sunrise"))
        returnData.append(json_extract(data, "sunset"))

    return returnData

def TimeAndWeather(locationString, detailed):
    locLatLong = GetLatLong(locationString)
    locTime = GetTime(locLatLong[0], locLatLong[1])
    locWeather = GetWeather(locLatLong[0], locLatLong[1], detailed)
    return locTime, locWeather

def GetData():
    returnData = []
    for location in locations:
        locTimeWeather = TimeAndWeather(location, True)
        returnData.append([location,locTimeWeather[0],locTimeWeather[1]])
        debugPrint(location)
        debugPrint(locTimeWeather[0])
        debugPrint(locTimeWeather[1])
        debugPrint("")
    return returnData

print(GetData())