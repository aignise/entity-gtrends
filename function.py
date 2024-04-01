import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_weather_forecast(location):
    find_places_url = "https://ai-weather-by-meteosource.p.rapidapi.com/find_places"
    find_places_querystring = {"text": location, "language": "en"}
    find_places_headers = {
        "X-RapidAPI-Key": os.getenv("X_RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
    }
    find_places_response = requests.get(find_places_url, headers=find_places_headers, params=find_places_querystring)

    if find_places_response.status_code == 200:
        first_location = find_places_response.json()[0]
        latitude = first_location['lat']
        longitude = first_location['lon']

        hourly_weather_url = "https://ai-weather-by-meteosource.p.rapidapi.com/hourly"
        hourly_weather_querystring = {
            "lat": latitude,
            "lon": longitude,
            "timezone": "auto",
            "language": "en",
            "units": "auto"
        }
        hourly_weather_headers = {
            "X-RapidAPI-Key": os.getenv("X_RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
        }
        hourly_weather_response = requests.get(hourly_weather_url, headers=hourly_weather_headers, params=hourly_weather_querystring)

        if hourly_weather_response.status_code == 200:
            return hourly_weather_response.json().get('hourly', {}).get('data', [])
        else:
            return None
    else:
        return None
