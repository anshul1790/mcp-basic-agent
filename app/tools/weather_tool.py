# app/tools/weather_tool.py

def get_weather(city: str) -> str:
    # Mocking a static response
    city = city.lower()
    weather_map = {
        "delhi": "Sunny, 34°C",
        "london": "Rainy, 17°C",
        "new york": "Cloudy, 22°C"
    }
    return weather_map.get(city, f"Weather data for {city} not available.")

tool_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"]
        }
    }
}
