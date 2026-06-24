import httpx

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# WMO weather codes -> human text (subset covering common cases)
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Freezing fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Dense drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}

# 16-point compass rose, each slice is 22.5 degrees
COMPASS_DIRS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
]


def aqi_category(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for sensitive groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very unhealthy"
    return "Hazardous"


def geocode_city(city: str) -> dict:
    """Returns {lat, lon, name, country} for the best match."""
    resp = httpx.get(GEOCODE_URL, params={"name": city, "count": 1})
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        raise ValueError(f"City not found: {city}")
    top = results[0]
    return {
        "lat": top["latitude"],
        "lon": top["longitude"],
        "name": top["name"],
        "country": top.get("country", ""),
    }


def get_forecast(lat: float, lon: float) -> dict:
    """Returns raw current + today's daily forecast block from Open-Meteo."""
    resp = httpx.get(FORECAST_URL, params={
        "latitude": lat,
        "longitude": lon,
        "current": (
            "temperature_2m,apparent_temperature,relative_humidity_2m,"
            "wind_speed_10m,wind_direction_10m,pressure_msl,weather_code"
        ),
        "daily": (
            "temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,uv_index_max,sunrise,sunset"
        ),
        "timezone": "auto",
        "forecast_days": 1,
    })
    resp.raise_for_status()
    return resp.json()


def get_aqi(lat: float, lon: float) -> dict:
    """Returns raw current AQI block from Open-Meteo Air Quality API."""
    resp = httpx.get(AIR_QUALITY_URL, params={
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi",
        "timezone": "auto",
    })
    resp.raise_for_status()
    return resp.json()


def weather_code_to_text(code: int) -> str:
    return WEATHER_CODES.get(code, "Unknown")


def degrees_to_compass(degrees: float) -> str:
    """Converts wind direction in degrees (0-360) to 16-point compass text."""
    idx = round(degrees / 22.5) % 16
    return COMPASS_DIRS[idx]