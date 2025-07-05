# scripts/extract.py
import requests
import pandas as pd
from pathlib import Path
from collections import defaultdict
from datetime import datetime

API_KEY = "ef4a9170516e8934770018479aae1707"
CITIES = ["Paris", "Tokyo", "Nairobi", "New York", "Antananarivo", "Sydney"]

# Définition des chemins absolus basés sur la position du script
BASE_DIR = Path(__file__).resolve().parent.parent  # remonte de scripts/ puis dags/
ACTUAL_WEATHER_DIR = BASE_DIR / "data" / "actual_weather"
HISTORICAL_SOURCE_DIR = BASE_DIR / "historical_source"
HISTORICAL_WEATHER_DIR = BASE_DIR / "data" / "historical_weather"
FORECAST_WEATHER_DIR = BASE_DIR / "data" / "forecast_weather"


def extract_actual_weather():
    data = []
    ACTUAL_WEATHER_DIR.mkdir(parents=True, exist_ok=True)

    for city in CITIES:
        try:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo_response = requests.get(geo_url).json()
            if not geo_response:
                print(f"City not found: {city}")
                continue

            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]

            weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            weather_response = requests.get(weather_url).json()

            entry = {
                "city": city,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "average temperature": weather_response["main"]["temp"],
                "min temperature": weather_response["main"]["temp_min"],
                "max temperature": weather_response["main"]["temp_max"],
                "humidity": weather_response["main"]["humidity"],
                "pressure": weather_response["main"]["pressure"],
                "wind speed": weather_response["wind"]["speed"],
                "description": weather_response["weather"][0]["description"]
            }
            data.append(entry)

        except Exception as e:
            print(f"Error for {city}: {e}")

    df = pd.DataFrame(data)
    df.to_csv(ACTUAL_WEATHER_DIR / "actual_weather.csv", index=False)
    print("✅ Actual weather data saved.")


def extract_historical_weather():
    folder = HISTORICAL_SOURCE_DIR
    mapping = {
        "paris_historic.xlsx": "Paris",
        "tokyo_historic.xlsx": "Tokyo",
        "nairobi_historic.xlsx": "Nairobi",
        "antananarivo_historic.xlsx": "Antananarivo",
        "new_york_historic.xlsx": "New York",
        "sydney_historic.xlsx": "Sydney"
    }

    dfs = []
    if not folder.exists():
        print(f"❌ Historical source folder not found at {folder}")
        return

    for file in folder.iterdir():
        if file.suffix == ".xlsx" and file.name in mapping:
            df = pd.read_excel(file)
            df["ville"] = mapping[file.name]
            df["time"] = pd.to_datetime(df["time"])
            dfs.append(df)

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        combined = combined.sort_values(by=["time", "ville"]).reset_index(drop=True)
        HISTORICAL_WEATHER_DIR.mkdir(parents=True, exist_ok=True)
        combined.to_csv(HISTORICAL_WEATHER_DIR / "historical_weather.csv", index=False)
        print("✅ Historical weather data saved.")
    else:
        print("⚠️ No historical Excel files found or loaded.")


def extract_forecast_weather():
    data = []
    FORECAST_WEATHER_DIR.mkdir(parents=True, exist_ok=True)

    for city in CITIES:
        try:
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
            geo_response = requests.get(geo_url).json()
            if not geo_response:
                print(f"City not found: {city}")
                continue

            lat = geo_response[0]["lat"]
            lon = geo_response[0]["lon"]

            forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
            forecast_response = requests.get(forecast_url).json()

            daily_data = defaultdict(list)
            for item in forecast_response["list"]:
                date_str = item["dt_txt"].split(" ")[0]
                daily_data[date_str].append(item)

            for date, items in daily_data.items():
                temps = [i["main"]["temp"] for i in items]
                min_temps = [i["main"]["temp_min"] for i in items]
                max_temps = [i["main"]["temp_max"] for i in items]
                humidities = [i["main"]["humidity"] for i in items]
                pressures = [i["main"]["pressure"] for i in items]
                wind_speeds = [i["wind"]["speed"] for i in items]
                descriptions = [i["weather"][0]["description"] for i in items]

                entry = {
                    "city": city,
                    "date": date,
                    "average temperature": sum(temps) / len(temps),
                    "min temperature": min(min_temps),
                    "max temperature": max(max_temps),
                    "humidity": sum(humidities) / len(humidities),
                    "pressure": sum(pressures) / len(pressures),
                    "wind speed": sum(wind_speeds) / len(wind_speeds),
                    "description": max(set(descriptions), key=descriptions.count)
                }
                data.append(entry)

        except Exception as e:
            print(f"Error for {city}: {e}")

    df = pd.DataFrame(data)
    df.to_csv(FORECAST_WEATHER_DIR / "forecast_weather.csv", index=False)
    print("✅ Forecast weather data saved.")


def extract():
    extract_actual_weather()
    extract_historical_weather()
    extract_forecast_weather()


if __name__ == "__main__":
    extract()
