from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import secrets
import requests
import json

def TimeAndWeather(locationString):
    geolocator = Nominatim(user_agent="geoapiExercises")
    print("Location Address:", locationString)
    location = geolocator.geocode(locationString)
    print("Long,Lat:", location.latitude, location.longitude)
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    print("Timezone:",result)
    IST = pytz.timezone(result)
    print("Current Time:", datetime.now(IST))
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&units=metric&appid={secrets.WEATHER_API}"
    response = requests.get(url)
    data = json.loads(response.text)
    print(data)
    print("")


locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "India"]
for location in locations:
    TimeAndWeather(location)