"""
weather.py — Day 3: 5 Day Forecast
"""

import requests
import os
from dotenv import load_dotenv
from rich.console import Console
from datetime import datetime

load_dotenv()
API_KEY      = os.getenv("API_KEY")
BASE_URL     = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
console      = Console()


def get_weather_emoji(condition: str) -> str:
    condition = condition.lower()
    if "clear" in condition:     return "☀️"
    elif "cloud" in condition:   return "⛅"
    elif "rain" in condition:    return "🌧️"
    elif "drizzle" in condition: return "🌦️"
    elif "thunder" in condition: return "⛈️"
    elif "snow" in condition:    return "❄️"
    elif "mist" in condition:    return "🌫️"
    elif "fog" in condition:     return "🌫️"
    elif "haze" in condition:    return "🌫️"
    else:                        return "🌡️"


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


def get_forecast(city: str):
    try:
        response = requests.get(FORECAST_URL, params={
            "q":     city,
            "appid": API_KEY,
            "units": "metric",
            "cnt":   40
        })

        data = response.json()

        if data["cod"] != "200":
            console.print(f"\n  [red]❌ {data['message'].title()}[/red]\n")
            return

        name    = data["city"]["name"]
        country = data["city"]["country"]

        console.print(f"\n  [bold white]5 Day Forecast — {name}, {country}[/bold white]")
        console.print(f"  [dim]────────────────────────────────[/dim]\n")

        # group by day — take first reading of each day
        seen_days = []
        for item in data["list"]:
            date     = datetime.fromtimestamp(item["dt"])
            day_name = date.strftime("%A")
            date_str = date.strftime("%b %d")

            if day_name not in seen_days:
                seen_days.append(day_name)

                temp_c    = item["main"]["temp"]
                temp_f    = celsius_to_fahrenheit(temp_c)
                condition = item["weather"][0]["description"]
                humidity  = item["main"]["humidity"]
                emoji     = get_weather_emoji(condition)

                console.print(f"  [bold cyan]{day_name:<10}[/bold cyan] [dim]{date_str}[/dim]")
                console.print(f"  {emoji}  {condition.title()}")
                console.print(f"  [yellow]{temp_c}°C[/yellow] · [yellow]{temp_f}°F[/yellow]   💧 [blue]{humidity}%[/blue]")
                console.print(f"  [dim]────────────────────────────────[/dim]")

        console.print()

    except Exception as e:
        console.print(f"  [red]❌ Something went wrong: {e}[/red]")


def main():
    console.print()
    console.print("  [bold cyan]PyWeather[/bold cyan]  [dim]——  Your simple weather app[/dim]")
    console.print("  [dim]────────────────────────────[/dim]")

    while True:
        console.print("\n  [bold]What do you want?[/bold]")
        console.print("  [yellow]1.[/yellow] Current weather")
        console.print("  [yellow]2.[/yellow] 5 day forecast")
        console.print("  [yellow]3.[/yellow] Both")
        console.print("  [yellow]4.[/yellow] Quit")

        choice = input("\n  Enter choice (1-4): ").strip()

        if choice == "4":
            console.print("\n  [cyan]👋 Goodbye![/cyan]\n")
            break

        if choice not in ["1", "2", "3"]:
            console.print("  [red]❌ Invalid choice.[/red]")
            continue

        city = input("  Enter city name: ").strip()
        if not city:
            console.print("  [red]❌ Please enter a city name.[/red]")
            continue

        if choice == "1":
            get_weather(city)
        elif choice == "2":
            get_forecast(city)
        elif choice == "3":
            get_weather(city)
            get_forecast(city)


if __name__ == "__main__":
    main()