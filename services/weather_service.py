"""
weather_service.py — Open-Meteo integration for WePet MVP.
Geocoding + current conditions + 12-hour hourly forecast.
"""
import requests
from datetime import datetime
from typing import Optional

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

CURRENT_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "wind_speed_10m",
    "uv_index",
    "is_day",
    "weather_code",
]

HOURLY_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "uv_index",
    "is_day",
]

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail",
}


def geocode_location(city: str) -> Optional[dict]:
    """Resolve city name → lat/lon/name via Open-Meteo Geocoding."""
    try:
        resp = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            return None
        r = results[0]
        return {
            "name": r.get("name", city),
            "country": r.get("country", ""),
            "admin1": r.get("admin1", ""),
            "latitude": r["latitude"],
            "longitude": r["longitude"],
            "display": f"{r.get('name', city)}, {r.get('admin1', '')}, {r.get('country', '')}".strip(", "),
        }
    except requests.RequestException as e:
        return {"error": f"Geocoding failed: {str(e)}"}


def fetch_weather(lat: float, lon: float) -> Optional[dict]:
    """Fetch current conditions + 12-hour hourly forecast from Open-Meteo."""
    try:
        resp = requests.get(
            FORECAST_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": ",".join(CURRENT_VARS),
                "hourly": ",".join(HOURLY_VARS),
                "forecast_days": 2,
                "timezone": "auto",
            },
            timeout=10,
        )
        resp.raise_for_status()
        raw = resp.json()

        current_raw = raw.get("current", {})
        current = {
            "temperature": current_raw.get("temperature_2m"),
            "humidity": current_raw.get("relative_humidity_2m"),
            "apparent_temperature": current_raw.get("apparent_temperature"),
            "wind_speed": current_raw.get("wind_speed_10m"),
            "uv_index": current_raw.get("uv_index", 0) or 0,
            "is_day": current_raw.get("is_day", 1),
            "weather_code": current_raw.get("weather_code", 0),
            "condition": WEATHER_CODES.get(current_raw.get("weather_code", 0), "Unknown"),
        }

        # Build 12-hour hourly forecast
        hourly_raw = raw.get("hourly", {})
        times = hourly_raw.get("time", [])
        now_str = datetime.now().strftime("%Y-%m-%dT%H")
        hourly = []

        # Find the current hour index
        start_idx = 0
        for i, t in enumerate(times):
            if t.startswith(now_str):
                start_idx = i
                break

        for i in range(start_idx, min(start_idx + 13, len(times))):
            hourly.append({
                "time": times[i],
                "hour_label": _fmt_hour(times[i]),
                "temperature": hourly_raw.get("temperature_2m", [])[i] if i < len(hourly_raw.get("temperature_2m", [])) else None,
                "humidity": hourly_raw.get("relative_humidity_2m", [])[i] if i < len(hourly_raw.get("relative_humidity_2m", [])) else None,
                "apparent_temperature": hourly_raw.get("apparent_temperature", [])[i] if i < len(hourly_raw.get("apparent_temperature", [])) else None,
                "uv_index": hourly_raw.get("uv_index", [])[i] if i < len(hourly_raw.get("uv_index", [])) else 0,
                "is_day": hourly_raw.get("is_day", [])[i] if i < len(hourly_raw.get("is_day", [])) else 1,
            })

        return {"current": current, "hourly": hourly}

    except requests.RequestException as e:
        return {"error": f"Weather fetch failed: {str(e)}"}


def _fmt_hour(time_str: str) -> str:
    """Format ISO hour string to readable label like '6:00 AM'."""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        return dt.strftime("%-I:%M %p")
    except Exception:
        try:
            dt = datetime.strptime(time_str[:13], "%Y-%m-%dT%H")
            return dt.strftime("%-I:%M %p")
        except Exception:
            return time_str


def get_weather_for_location(city: str) -> dict:
    """Full pipeline: city → geocode → weather. Returns structured result or error."""
    geo = geocode_location(city)
    if not geo or "error" in geo:
        return {"error": geo.get("error", "Location not found. Please try a different city name.")}

    weather = fetch_weather(geo["latitude"], geo["longitude"])
    if not weather or "error" in weather:
        return {"error": weather.get("error", "Weather data unavailable. Please try again.")}

    return {
        "location": geo,
        "current": weather["current"],
        "hourly": weather["hourly"],
    }