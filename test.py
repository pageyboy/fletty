from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz

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
    print("")


locations = ["Middlewich, UK", "Colorado Springs, Colorado", "Tokyo, Japan", "Melbourne, Australia", "Cupertino, California", "India"]
for location in locations:
    TimeAndWeather(location)