# # backend/services/weather_service.py
# import os
# import requests
# from dotenv import load_dotenv
# from .alert_logic import generate_weather_alert

# load_dotenv()
# API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# # FUNCTION 1: For the Dashboard Weather Alert Card
# def get_weather_by_city(city: str) -> dict:
#     if not API_KEY: raise ValueError("OpenWeatherMap API key not set.")
#     params = {"q": city, "appid": API_KEY, "units": "metric"}
#     response = requests.get(BASE_URL, params=params)
#     response.raise_for_status()
#     data = response.json()
#     weather_info = {
#         "city": data["name"], "temperature": data["main"]["temp"],
#         "description": data["weather"][0]["description"].title(),
#         "humidity": data["main"]["humidity"], "wind_speed": data["wind"]["speed"]
#     }
#     alert_message = generate_weather_alert(weather_info)
#     weather_info["alert"] = alert_message
#     return weather_info

# # FUNCTION 2: A simple helper for the recommendation models
# def get_weather_data_for_model(city: str) -> dict:
#     if not API_KEY: raise ValueError("OpenWeatherMap API key not set.")
#     params = {"q": city, "appid": API_KEY, "units": "metric"}
#     try:
#         response = requests.get(BASE_URL, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"]}
#     except Exception:
#         print(f"Weather API failed for {city}, using default values for model.")
#         return {"temperature": 25.0, "humidity": 60.0}

import os
import requests
from dotenv import load_dotenv
# Ensure alert_logic.py is in the same directory
from .alert_logic import generate_weather_alert 

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# FUNCTION 1: Optimized for the Dashboard Weather Alert Card
def get_weather_by_city(city: str) -> dict:
    if not API_KEY: 
        raise ValueError("OpenWeatherMap API key not set in .env file.")
        
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            "city": data["name"], 
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"], 
            "wind_speed": data["wind"]["speed"],
            "pressure": data["main"]["pressure"],
            # CRITICAL: Include rainfall in the dashboard response so frontend context can store it
            "rainfall": data.get("rain", {}).get("1h", 0.0) 
        }
        
        alert_message = generate_weather_alert(weather_info)
        weather_info["alert"] = alert_message
        return weather_info
    except requests.exceptions.HTTPError as err:
         if err.response.status_code == 401:
              raise ValueError("Invalid OpenWeatherMap API key.")
         elif err.response.status_code == 404:
              raise ValueError(f"City '{city}' not found.")
         else:
              raise Exception(f"Weather API HTTP error: {err}")
    except Exception as e:
        raise Exception(f"Failed to get weather alert data: {e}")

# FUNCTION 2: Helper for the KrushiVaani ML Recommendation models
def get_weather_data_for_model(city: str) -> dict:
    """
    Fetches temperature, humidity, and rainfall for the ML model.
    Ensures 'rainfall' is always present for the Random Forest 7-feature input.
    """
    if not API_KEY: 
        raise ValueError("OpenWeatherMap API key not set.")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # ML CRITICAL: Extract rainfall. 
        # OpenWeather returns 'rain' only if it is currently raining.
        rain_data = data.get("rain", {})
        # We prioritize 1h rain data; if none, we use 0.0 (realistic for current state)
        rainfall = rain_data.get("1h", 0.0) 

        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": rainfall
        }
    except Exception as e:
        print(f"DEBUG: Weather API failed for {city}: {e}. Using ML fallback defaults.")
        # Fallbacks aligned with common Indian agricultural data averages
        return {
            "temperature": 25.0, 
            "humidity": 70.0, 
            "rainfall": 100.0
        }