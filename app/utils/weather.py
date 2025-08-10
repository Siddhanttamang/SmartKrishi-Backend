import requests
import os

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise Exception("Missing OPENWEATHER_API_KEY in environment")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "City not found or API error"}

    data = response.json()
    return {
        "city": data["name"],
        "temperature": int(data["main"]["temp"]),
        "feels_like": int(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"]
    }


