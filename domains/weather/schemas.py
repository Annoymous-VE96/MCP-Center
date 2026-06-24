from pydantic import BaseModel, Field


class WeatherBriefInput(BaseModel):
    city: str = Field(..., description="City name, e.g. 'Mumbai' or 'London,UK'")


class WeatherBriefOutput(BaseModel):
    city: str
    country: str
    condition: str            
    temp_now_c: float
    feels_like_c: float
    humidity_pct: int
    wind_kph: float
    wind_direction: str       
    pressure_hpa: float
    uv_index: float
    high_c: float
    low_c: float
    precip_chance_pct: int
    sunrise: str               
    sunset: str                 
    aqi: int
    aqi_category: str         