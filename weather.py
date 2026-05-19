"""
weather.py — Day 1: Basic Weather App
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):
    try:
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"  # celsius
        })

        data = response.json()

        if data["cod"] != 200:
            print(f"❌ Error: {data['message']}")
            return

        # extract info
        name        = data["name"]
        country     = data["sys"]["country"]
        temp        = data["main"]["temp"]
        feels_like  = data["main"]["feels_like"]
        humidity    = data["main"]["humidity"]
        condition   = data["weather"][0]["description"]
        wind_speed  = data["wind"]["speed"]

        # display
        print(f"\n📍 {name}, {country}")
        print(f"🌤  Condition  : {condition.title()}")
        print(f"🌡  Temperature: {temp}°C (Feels like {feels_like}°C)")
        print(f"💧 Humidity   : {humidity}%")
        print(f"💨 Wind Speed : {wind_speed} m/s")
        print()

    except Exception as e:
        print(f"❌ Something went wrong: {e}")


def main():
    print("=" * 40)
    print("   🌤  PyWeather — Day 1")
    print("=" * 40)

    while True:
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        if city.lower() == "quit":
            print("👋 Goodbye!")
            break
        if not city:
            print("❌ Please enter a city name.")
            continue
        get_weather(city)


if __name__ == "__main__":
    main()