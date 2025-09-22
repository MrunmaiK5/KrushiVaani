# backend/services/weather_service.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_by_city(city: str) -> dict:
    """Fetches and simplifies weather data for a given city."""
    if not API_KEY:
        raise ValueError("OpenWeatherMap API key not found. Please check your .env file.")

    params = {"q": city, "appid": API_KEY, "units": "metric"} # units=metric for Celsius

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        data = response.json()
        
        # Simplify the response to only what our frontend needs
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"City '{city}' not found.")
        elif e.response.status_code == 401:
            raise ValueError("Invalid API key. Please check your .env file and wait a few minutes for it to activate.")
        else:
            raise Exception(f"Failed to get weather data (Status code: {e.response.status_code})")
    except requests.exceptions.RequestException:
        raise Exception("A network error occurred while fetching weather data.")