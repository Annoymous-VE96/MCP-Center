from domains.weather.tools import get_weather_tool
from domains.weather.schemas import WeatherBriefInput

result = get_weather_tool(WeatherBriefInput(city="Howrah"))
print(result.model_dump_json(indent=2))