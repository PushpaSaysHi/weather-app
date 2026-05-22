"""
weather.py — Day 4: Favorite Cities
"""

import requests
import os
import json
from dotenv import load_dotenv
from rich.console import Console
from datetime import datetime

load_dotenv()
API_KEY      = os.getenv("API_KEY")
BASE_URL     = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
FAVORITES_FILE = "favorites.json"
console      = Console()


# ── Favorites ────────────────────────────────────────────────

def load_favorites() -> list:
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)


def save_favorites(favorites: list):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)


def add_favorite(city: str):
    favorites = load_favorites()
    if city.lower() in [f.lower() for f in favorites]:
        console.print(f"  [yellow]⚠️  {city} is already in favorites![/yellow]")
        return
    favorites.append(city)
    save_favorites(favorites)
    console.print(f"  [green]✅ {city} added to favorites![/green]")


def remove_favorite(city: str):
    favorites = load_favorites()
    for f in favorites:
        if f.lower() == city.lower():
            favorites.remove(f)
            save_favorites(favorites)
            console.print(f"  [green]✅ {city} removed from favorites![/green]")
            return
    console.print(f"  [red]❌ {city} not found in favorites.[/red]")


def show_favorites():
    favorites = load_favorites()
    if not favorites:
        console.print("  [dim]No favorites yet![/dim]")
        return
    console.print("\n  [bold white]⭐ Favorite Cities[/bold white]")
    console.print("  [dim]──────────────[/dim]")
    for i, city in enumerate(favorites, 1):
        console.print(f"  [yellow]{i}.[/yellow] {city}")
    console.print()


def weather_all_favorites():
    favorites = load_favorites()
    if not favorites:
        console.print("  [dim]No favorites yet! Add some cities first.[/dim]")
        return
    for city in favorites:
        get_weather(city)


# ── Helpers ──────────────────────────────────────────────────

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


# ── Weather ──────────────────────────────────────────────────

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


# ── Main ─────────────────────────────────────────────────────

def main():
    console.print()
    console.print("  [bold cyan]PyWeather[/bold cyan]  [dim]——  Your simple weather app[/dim]")
    console.print("  [dim]────────────────────────────[/dim]")

    while True:
        console.print("\n  [bold]What do you want?[/bold]")
        console.print("  [yellow]1.[/yellow] Current weather")
        console.print("  [yellow]2.[/yellow] 5 day forecast")
        console.print("  [yellow]3.[/yellow] Both")
        console.print("  [yellow]4.[/yellow] Add city to favorites")
        console.print("  [yellow]5.[/yellow] Remove city from favorites")
        console.print("  [yellow]6.[/yellow] Show favorites")
        console.print("  [yellow]7.[/yellow] Weather for all favorites")
        console.print("  [yellow]8.[/yellow] Quit")

        choice = input("\n  Enter choice (1-8): ").strip()

        if choice == "8":
            console.print("\n  [cyan]👋 Goodbye![/cyan]\n")
            break

        elif choice in ["1", "2", "3"]:
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

        elif choice == "4":
            city = input("  Enter city to add to favorites: ").strip()
            if city:
                add_favorite(city)

        elif choice == "5":
            show_favorites()
            city = input("  Enter city to remove: ").strip()
            if city:
                remove_favorite(city)

        elif choice == "6":
            show_favorites()

        elif choice == "7":
            weather_all_favorites()

        else:
            console.print("  [red]❌ Invalid choice.[/red]")


if __name__ == "__main__":
    main()