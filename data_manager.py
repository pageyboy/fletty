from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import secrets
import requests
import json
from extract import json_extract

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
    returnData = {}
    returnData["description"] = json_extract(data, "description")[0]
    if detailed == True:
        returnData["temp"] = json_extract(data, "temp")[0]
        returnData["windspeed"] = json_extract(data, "speed")[0]
        returnData["sunrise"] = json_extract(data, "sunrise")[0]
        returnData["sunset"] = json_extract(data, "sunset")[0]

    return returnData

def TimeAndWeather(locationString, detailed):
    locLatLong = GetLatLong(locationString)
    locTime = GetTime(locLatLong[0], locLatLong[1])
    locWeather = GetWeather(locLatLong[0], locLatLong[1], detailed)
    return locTime, locWeather

def GetData(locations):
    dataList = []
    dataDict = {}
    for location in locations:
        locTimeWeather = TimeAndWeather(location, True)
        dataDict["location"] = location
        dataDict["time"] = locTimeWeather[0]
        dataDict["weather"] = locTimeWeather[1]
        dataList.append(dataDict)
        dataDict = {}
        debugPrint(location)
        debugPrint(locTimeWeather[0])
        debugPrint(locTimeWeather[1])
        debugPrint("")
    returnData = {}
    returnData["locations"] = dataList
    return(returnData)