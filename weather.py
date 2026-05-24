"""
weather_gui.py — PyWeather GUI using CustomTkinter
"""

import customtkinter as ctk
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY        = os.getenv("API_KEY")
BASE_URL       = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL   = "https://api.openweathermap.org/data/2.5/forecast"
FAVORITES_FILE = "favorites.json"

# ── Appearance ───────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


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


def get_current_location():
    try:
        response = requests.get("https://ipapi.co/json/")
        data     = response.json()
        return data.get("city", None)
    except:
        return None


def load_favorites() -> list:
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)


def save_favorites(favorites: list):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)


# ── Main App ─────────────────────────────────────────────────

class PyWeatherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PyWeather")
        self.geometry("500x700")
        self.resizable(False, False)

        self._build_ui()
        self._auto_detect_location()

    def _build_ui(self):

        # ── Header ───────────────────────────────────────────
        self.header = ctk.CTkLabel(
            self, text="🌤  PyWeather",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.header.pack(pady=(20, 20))

        

        # ── Search bar ───────────────────────────────────────
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(padx=20, fill="x")

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.city_entry.bind("<Return>", lambda e: self._search_weather())

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=90,
            height=40,
            command=self._search_weather
        )
        self.search_btn.pack(side="right")

        # ── Tabs ─────────────────────────────────────────────
        self.tabs = ctk.CTkTabview(self, height=420)
        self.tabs.pack(padx=20, pady=15, fill="both", expand=True)
        self.tabs.add("Current")
        self.tabs.add("Forecast")
        self.tabs.add("Favorites")

        self._build_current_tab()
        self._build_forecast_tab()
        self._build_favorites_tab()

    # ── Current tab ──────────────────────────────────────────

    def _build_current_tab(self):
        tab = self.tabs.tab("Current")

        self.location_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.location_label.pack(pady=(20, 5))

        self.emoji_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=36)
        )
        self.emoji_label.pack(pady=5)

        self.condition_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.condition_label.pack(pady=5)

        self.temp_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.temp_label.pack(pady=5)

        self.feels_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.feels_label.pack(pady=2)

        # humidity and wind
        self.details_frame = ctk.CTkFrame(tab)
        self.details_frame.pack(pady=15, padx=20, fill="x")

        self.humidity_label = ctk.CTkLabel(
            self.details_frame, text="",
            font=ctk.CTkFont(size=14)
        )
        self.humidity_label.pack(side="left", expand=True)

        self.wind_label = ctk.CTkLabel(
            self.details_frame, text="",
            font=ctk.CTkFont(size=14)
        )
        self.wind_label.pack(side="right", expand=True)

        self.fav_btn = ctk.CTkButton(
            tab,
            text="⭐ Add to Favorites",
            command=self._add_to_favorites
        )
        self.fav_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            tab, text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status_label.pack()

    # ── Forecast tab ─────────────────────────────────────────

    def _build_forecast_tab(self):
        tab = self.tabs.tab("Forecast")

        self.forecast_frame = ctk.CTkScrollableFrame(tab)
        self.forecast_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # ── Favorites tab ────────────────────────────────────────

    def _build_favorites_tab(self):
        tab = self.tabs.tab("Favorites")

        self.favorites_frame = ctk.CTkScrollableFrame(tab)
        self.favorites_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self._refresh_favorites()

    def _refresh_favorites(self):
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()

        favorites = load_favorites()
        if not favorites:
            ctk.CTkLabel(
                self.favorites_frame,
                text="No favorites yet!\nSearch a city and click ⭐",
                text_color="gray"
            ).pack(pady=20)
            return

        for city in favorites:
            row = ctk.CTkFrame(self.favorites_frame)
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row, text=city,
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=10, pady=8)

            ctk.CTkButton(
                row, text="View",
                width=60, height=28,
                command=lambda c=city: self._load_city(c)
            ).pack(side="right", padx=5, pady=5)

            ctk.CTkButton(
                row, text="🗑",
                width=40, height=28,
                fg_color="red", hover_color="darkred",
                command=lambda c=city: self._remove_favorite(c)
            ).pack(side="right", padx=5, pady=5)

    # ── Actions ──────────────────────────────────────────────

    def _auto_detect_location(self):
        self.status_label.configure(text="📍 Detecting location...")
        city = get_current_location()
        if city:
            self.city_entry.insert(0, city)
            self._search_weather()

    def _load_city(self, city: str):
        self.city_entry.delete(0, "end")
        self.city_entry.insert(0, city)
        self._search_weather()
        self.tabs.set("Current")

    def _search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.status_label.configure(text="❌ Please enter a city name.")
            return
        self._fetch_current(city)
        self._fetch_forecast(city)

    def _fetch_current(self, city: str):
        try:
            response = requests.get(BASE_URL, params={
                "q": city, "appid": API_KEY, "units": "metric"
            })
            data = response.json()

            if data["cod"] != 200:
                self.status_label.configure(text=f"❌ {data['message'].title()}")
                return

            self.current_city    = data["name"]
            country    = data["sys"]["country"]
            temp_c     = data["main"]["temp"]
            feels_c    = data["main"]["feels_like"]
            temp_f     = celsius_to_fahrenheit(temp_c)
            feels_f    = celsius_to_fahrenheit(feels_c)
            humidity   = data["main"]["humidity"]
            condition  = data["weather"][0]["description"]
            wind_speed = data["wind"]["speed"]
            emoji      = get_weather_emoji(condition)

            self.location_label.configure(text=f"📍 {self.current_city}, {country}")
            self.emoji_label.configure(text=emoji)
            self.condition_label.configure(text=condition.title())
            self.temp_label.configure(text=f"{temp_c}°C  ·  {temp_f}°F")
            self.feels_label.configure(text=f"Feels like {feels_c}°C / {feels_f}°F")
            self.humidity_label.configure(text=f"💧 Humidity: {humidity}%")
            self.wind_label.configure(text=f"💨 Wind: {wind_speed} m/s")
            self.status_label.configure(text="")

        except Exception as e:
            self.status_label.configure(text=f"❌ {e}")

    def _fetch_forecast(self, city: str):
        try:
            response = requests.get(FORECAST_URL, params={
                "q": city, "appid": API_KEY, "units": "metric", "cnt": 40
            })
            data = response.json()

            if data["cod"] != "200":
                return

            for widget in self.forecast_frame.winfo_children():
                widget.destroy()

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

                    row = ctk.CTkFrame(self.forecast_frame)
                    row.pack(fill="x", pady=4, padx=5)

                    ctk.CTkLabel(
                        row,
                        text=f"{day_name}  {date_str}",
                        font=ctk.CTkFont(size=13, weight="bold")
                    ).pack(side="left", padx=10, pady=8)

                    ctk.CTkLabel(
                        row,
                        text=f"{emoji} {condition.title()}",
                        font=ctk.CTkFont(size=13)
                    ).pack(side="left", padx=10)

                    ctk.CTkLabel(
                        row,
                        text=f"{temp_c}°C · {temp_f}°F  💧{humidity}%",
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    ).pack(side="right", padx=10)

        except Exception as e:
            pass

    def _add_to_favorites(self):
        if hasattr(self, "current_city") and self.current_city:
            favorites = load_favorites()
            if self.current_city.lower() not in [f.lower() for f in favorites]:
                favorites.append(self.current_city)
                save_favorites(favorites)
                self.status_label.configure(text=f"⭐ {self.current_city} added to favorites!")
            else:
                self.status_label.configure(text=f"⚠️ Already in favorites!")
            self._refresh_favorites()

    def _remove_favorite(self, city: str):
        favorites = load_favorites()
        favorites = [f for f in favorites if f.lower() != city.lower()]
        save_favorites(favorites)
        self._refresh_favorites()


# ── Run ──────────────────────────────────────────────────────

if __name__ == "__main__":
    app = PyWeatherApp()
    app.mainloop()