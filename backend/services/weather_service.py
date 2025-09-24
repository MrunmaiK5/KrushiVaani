# backend/services/weather_service.py
import os
import requests
from dotenv import load_dotenv

# NEW: Import your alert generation function from the same directory
from .alert_logic import generate_weather_alert

# Load environment variables from the .env file in the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city: str) -> dict:
    """Fetches, simplifies, and analyzes weather data for a given city."""
    if not API_KEY:
        raise ValueError("OpenWeatherMap API key not found. Please check your .env file.")

    params = {"q": city, "appid": API_KEY, "units": "metric"} # units=metric for Celsius

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # MODIFIED: The dictionary is created first to pass to your function
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
        # NEW: Call your function using the simplified weather data
        alert_message = generate_weather_alert(weather_info)
        
        # NEW: Add the returned alert message to the dictionary
        weather_info["alert"] = alert_message
        
        # Return the final dictionary, now including your alert
        return weather_info
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"City '{city}' not found.")
        elif e.response.status_code == 401:
            raise ValueError("Invalid API key. Please check your .env file and wait a few minutes for it to activate.")
        else:
            raise Exception(f"Failed to get weather data (Status code: {e.response.status_code})")
    except requests.exceptions.RequestException:
        raise Exception("A network error occurred while fetching weather data.")