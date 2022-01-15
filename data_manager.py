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
    """
    Wrapper function to bulk enable disable debug prints.
    if the debug flag is enabled then the message is outputted

    Args:
        message (string): message to output
    """
    if debug == True:
        print(message)

def GetLatLong(locationString):
    """
    Get the latitude and longitude from a given location string

    Args:
        locationString (string): Location string to evaluate (i.e. Middlewich, UK)

    Returns:
        [type]: [description]
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    debugPrint("Location Address:" + locationString)
    location = geolocator.geocode(locationString)
    debugPrint("Long,Lat:" + str(location.latitude) + " " + str(location.longitude))
    return [location.latitude, location.longitude]

def formatTime(date, epoch, timezone):
    """
    Format the time as a string such that display code doesn't need
    to use timezone and UTC information to determine the time.
    If the time is left as UTC with timezone information then Flask outputs
    ONLY the UTC time

    Args:
        date (datetime): date in datetime format
        epoch (boolean): if the incoming date is an epoch time
        timezone (pytz.timezone): timezone in pytz format

    Returns:
        string: time formatted as hh:mm
    """
    if epoch:
        date = datetime.fromtimestamp(date, tz=timezone)
    date = f"{date.hour:02d}" + ":" + f"{date.minute:02d}"
    return date

def GetTime(latitude, longitude):
    """
    Get the time at a given longitude / latitude

    Args:
        latitude ([pytz.latitude]): latitude returned by pytz.timezone_at()
        longitude ([pytz.longitude]): longitude returned by pytz.timezone_at()

    Returns:
        [datetime, pytz.timezone]: returns datetime & pytz.timezone in a list
    """
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=latitude, lng=longitude)
    debugPrint("Timezone:" + str(result))
    tz = pytz.timezone(result)
    date = formatTime(datetime.now(tz), False, None)
    debugPrint("Current Time:" + date)
    return date, tz

def GetWeather(latitude, longitude, detailed, tz):
    """
    Get the weather utilizing openweathermap API at a given longitude and latitude.
    Can provide detailed information depending on detailed flag

    Args:
        latitude (pytz.latitude): pytz.latitude
        longitude (pytz.longitude): pytz.longitude
        detailed (boolean): flag for whether the returned weather should be detailed or not
        tz (pytz.timezone): pytz.timezone. Used for converting sunset, sunrise information
                            which is returned in epoch format

    Returns:
        detailed == False
        [string]: description of weather

        detailed == True
        [string]: description of weather
        [numeric]: temp
        [numeric]: windspeed
        [string]: sunrise in local time formatted as hh:mm
        [string]: sunset in local time formatted as hh:mm
        [numeric]: minimum temperature
        [numeric]: maximum temperature
        [numeric]: humidity
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={secrets.WEATHER_API}"
    response = requests.get(url)
    data = json.loads(response.text)
    returnData = {}
    returnData["description"] = json_extract(data, "description")[0]
    if detailed == True:
        returnData["temp"] = json_extract(data, "temp")[0]
        returnData["windspeed"] = json_extract(data, "speed")[0]
        returnData["sunrise"] = formatTime(json_extract(data, "sunrise")[0], True, tz)
        returnData["sunset"] = formatTime(json_extract(data, "sunset")[0], True, tz)
        returnData["min_temp"] = json_extract(data, "temp_min")[0]
        returnData["max_temp"] = json_extract(data, "temp_max")[0]
        returnData["humidity"] = json_extract(data, "humidity")[0]

    return returnData

def TimeAndWeather(locationString, detailed):
    """
    Wrapper function to get Time and Weather

    Args:
        locationString (string): Location string to evaluate (i.e. Middlewich, UK)
        detailed (boolean): Flag to denote whether the weather returned is detailed or not

    Returns:
        [type]: [description]
    """
    locLatLong = GetLatLong(locationString)
    locTime = GetTime(locLatLong[0], locLatLong[1])
    locWeather = GetWeather(locLatLong[0], locLatLong[1], detailed, locTime[1])
    return locTime[0], locWeather

def GetData(locations):
    """
    Function to be called by flask when page is queried


    Args:
        locations ([string]): list of location strings

    Returns:
        [{location, time, [weather]}]: dictionary of locations with a list of weather conditions
    """
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
    return returnData