import urllib.request
import json


def get_weather(latitude, longitude):
    """
    Fetch current temperature and humidity from Open-Meteo.
    Free, no API key needed.
    Returns a dict or None if the request fails.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,weather_code"
        f"&forecast_days=1"
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read())
            current = data.get("current", {})
            temp = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            weather_code = current.get("weather_code", 0)

            return {
                "temperature": temp,
                "humidity": humidity,
                "weather_code": weather_code,
                "description": _weather_description(weather_code),
                "temp_warning": temp is not None and temp > 60,
                "humidity_warning": humidity is not None and humidity > 85,
            }
    except Exception:
        return None


def _weather_description(code):
    """Map Open-Meteo WMO weather codes to human-readable strings."""
    descriptions = {
        0:  "Clear sky",
        1:  "Mainly clear",
        2:  "Partly cloudy",
        3:  "Overcast",
        45: "Foggy",
        48: "Icy fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight showers",
        81: "Moderate showers",
        82: "Violent showers",
        95: "Thunderstorm",
        99: "Thunderstorm with hail",
    }
    return descriptions.get(code, "Unknown")