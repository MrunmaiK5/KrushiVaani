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
# Assuming alert_logic.py is in the same directory
from .alert_logic import generate_weather_alert 

load_dotenv()
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# FUNCTION 1: For the Dashboard Weather Alert Card
def get_weather_by_city(city: str) -> dict:
    if not API_KEY: 
        raise ValueError("OpenWeatherMap API key not set in .env file.")
        
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raises HTTPError for bad responses (4XX, 5XX)
        data = response.json()
        
        weather_info = {
            "city": data["name"], 
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"], 
            "wind_speed": data["wind"]["speed"] # Speed is in m/s
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

# FUNCTION 2: Helper for the recommendation models
def get_weather_data_for_model(city: str) -> dict:
    if not API_KEY: 
        raise ValueError("OpenWeatherMap API key not set in .env file.")

    params = {"q": city, "appid": API_KEY, "units": "metric"}
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"]
        }
    except Exception:
        # Log the error but return defaults so recommendation doesn't completely fail
        print(f"Weather API failed for {city}, using default values for model.")
        return {"temperature": 25.0, "humidity": 60.0} # Sensible defaults
