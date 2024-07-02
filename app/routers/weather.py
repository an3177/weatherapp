from fastapi import APIRouter, Depends, Query, HTTPException
from ..oauth2 import get_current_user
import requests
from ..config import settings
from typing import List

router = APIRouter()

API_KEY = settings.api_key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@router.get("/getweather/", dependencies=[Depends(get_current_user)])
def get_weather_city(city: str = Query(title="City", description="Query string for the weather to search based on City")):
    params = {'q': city,
              'appid': API_KEY,
              'unites': 'metric'}
    weather_info = {}
    response = requests.get(BASE_URL, params = params)
    if response.status_code == 200:
        data = response.json()
        weather_info["city"] = data["name"],
        weather_info["temperature"] = data["main"]["temp"],
        weather_info["description"] = data["weather"][0]["description"],
        weather_info["humidity"] = data["main"]["humidity"]
        weather_info["wind_speed"] = data["wind"]["speed"]
        return weather_info
    else:
        raise HTTPException(status_code=404, detail="City not found")
    
@router.get("/getweathers/", dependencies=[Depends(get_current_user)])
def get_weather_cities(cities: List[str] = Query(default=[], title="List of City", description="Query string for the weather to search based on list of city")):
    params = {'q': cities}
    weather_list = []
    for city in cities:
        weather_list.append(get_weather_city(city))
    return weather_list