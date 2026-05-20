"""
weather.py — Day 2: Minimal Clean Style
"""

import requests
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text

load_dotenv()
API_KEY  = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
console  = Console()


def get_weather_emoji(condition: str) -> str:
    condition = condition.lower()
    if "clear" in condition:       return "☀️"
    elif "cloud" in condition:     return "⛅"
    elif "rain" in condition:      return "🌧️"
    elif "drizzle" in condition:   return "🌦️"
    elif "thunder" in condition:   return "⛈️"
    elif "snow" in condition:      return "❄️"
    elif "mist" in condition:      return "🌫️"
    elif "fog" in condition:       return "🌫️"
    elif "haze" in condition:      return "🌫️"
    else:                          return "🌡️"


def celsius_to_fahrenheit(c: float) -> float:
    return round((c * 9/5) + 32, 1)


def get_weather(city: str):
    try:
        response = requests.get(BASE_URL, params={
            "q":     city,
            "appid": API_KEY,
            "units": "metric"
        })

        data = response.json()

        if data["cod"] != 200:
            console.print(f"\n  [red]❌ {data['message'].title()}[/red]\n")
            return

        name       = data["name"]
        country    = data["sys"]["country"]
        temp_c     = data["main"]["temp"]
        feels_c    = data["main"]["feels_like"]
        temp_f     = celsius_to_fahrenheit(temp_c)
        feels_f    = celsius_to_fahrenheit(feels_c)
        humidity   = data["main"]["humidity"]
        condition  = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]
        emoji      = get_weather_emoji(condition)

        console.print(f"\n  [bold white]{name}, {country}[/bold white]")
        console.print(f"  [dim]──────────────[/dim]")
        console.print(f"  {emoji}  [cyan]{condition.title()}[/cyan]")
        console.print(f"  [bold yellow]{temp_c}°C[/bold yellow] · [yellow]{temp_f}°F[/yellow]  [dim]Feels like {feels_c}°C[/dim]")
        console.print(f"  💧 [blue]{humidity}%[/blue]   💨 [green]{wind_speed} m/s[/green]")
        console.print()

    except Exception as e:
        console.print(f"  [red]❌ Something went wrong: {e}[/red]")


def main():
    console.print()
    console.print("  [bold cyan]PyWeather[/bold cyan]  [dim]——  Your simple weather app[/dim]")
    console.print("  [dim]────────────────────────────[/dim]")

    while True:
        city = input("\n  Enter city (or 'quit' to exit): ").strip()
        if city.lower() == "quit":
            console.print("\n  [cyan]👋 Goodbye![/cyan]\n")
            break
        if not city:
            console.print("  [red]❌ Please enter a city name.[/red]")
            continue
        get_weather(city)


if __name__ == "__main__":
    main()