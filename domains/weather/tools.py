from domains.weather.client import (
    geocode_city, get_forecast, get_aqi,
    weather_code_to_text, degrees_to_compass, aqi_category,
)
from domains.weather.schemas import WeatherBriefInput, WeatherBriefOutput


def get_weather_tool(input: WeatherBriefInput) -> WeatherBriefOutput:
    """
    Gets the weather update for today
    input: city name
    output: humidity, temperature, real feel, wind speed and many more 
    """
    loc = geocode_city(input.city)
    data = get_forecast(loc['lat'], loc['lon'])
    air = get_aqi(loc['lat'], loc['lon'])

    current = data['current']
    daily = data['daily']

    return WeatherBriefOutput(
        city=loc['name'],
        country=loc['country'],
        condition=weather_code_to_text(current['weather_code']),
        temp_now_c=current['temperature_2m'],
        feels_like_c=current['apparent_temperature'],
        humidity_pct=current['relative_humidity_2m'],
        wind_kph=current['wind_speed_10m'],
        wind_direction=degrees_to_compass(current['wind_direction_10m']),
        pressure_hpa=current['pressure_msl'],
        uv_index=daily['uv_index_max'][0],
        high_c=daily['temperature_2m_max'][0],
        low_c=daily['temperature_2m_min'][0],
        precip_chance_pct=daily['precipitation_probability_max'][0],
        sunrise=daily['sunrise'][0],
        sunset=daily['sunset'][0],
        aqi=air['current']['us_aqi'],
        aqi_category=aqi_category(air['current']['us_aqi']),
    )