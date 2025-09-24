# backend/services/alert_logic.py

def generate_weather_alert(weather_data: dict) -> str:
    """
    Analyzes weather data and returns a prioritized, actionable alert for a farmer.
    
    Args:
        weather_data: A dictionary containing simplified weather info.
        
    Returns:
        A string containing the alert message.
    """
    
    # --- Prepare the data ---
    temp = weather_data.get("temperature", 0)
    humidity = weather_data.get("humidity", 0)
    
    # Convert wind speed from m/s (from API) to km/h for our logic
    wind_ms = weather_data.get("wind_speed", 0)
    wind_kmh = round(wind_ms * 3.6, 1)
    
    # Create a simple rain chance value based on the description
    description = weather_data.get("description", "").lower()
    rain_chance = 100 if "rain" in description else 0

    # --- Apply Rules (Highest priority first) ---
    if temp > 38:
        return f"🔥 Extreme Heat Alert: Temperature is {temp}°C. Ensure crops receive extra water today."
        
    if rain_chance > 70:
        return f"🌧️ Heavy Rain Alert: High chance of rain. Check field drainage to prevent waterlogging."

    if wind_kmh > 30:
        return f"💨 Strong Wind Warning: Wind speeds of {wind_kmh} km/h expected. Secure tall crops."
        
    if temp < 12:
        return f"❄️ Low Temperature Alert: Temperature may drop to {temp}°C. Protect young or sensitive plants."

    if humidity > 85:
        return f"💧 High Humidity Notice: Humidity is at {humidity}%. Be vigilant for signs of fungal disease."

    # --- Default Message ---
    return "✅ Weather looks clear. No critical alerts for your farm right now."