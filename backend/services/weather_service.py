# backend/services/weather_service.py
import os
import requests
from dotenv import load_dotenv
from .alert_logic import generate_weather_alert

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# FUNCTION 1: For the Dashboard Weather Alert Card
def get_weather_by_city(city: str) -> dict:
    if not API_KEY: raise ValueError("OpenWeatherMap API key not set.")
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    weather_info = {
        "city": data["name"], "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"].title(),
        "humidity": data["main"]["humidity"], "wind_speed": data["wind"]["speed"]
    }
    alert_message = generate_weather_alert(weather_info)
    weather_info["alert"] = alert_message
    return weather_info

# FUNCTION 2: A simple helper for the recommendation models
def get_weather_data_for_model(city: str) -> dict:
    if not API_KEY: raise ValueError("OpenWeatherMap API key not set.")
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"]}
    except Exception:
        print(f"Weather API failed for {city}, using default values for model.")
        return {"temperature": 25.0, "humidity": 60.0}