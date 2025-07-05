# scripts/transform.py
import pandas as pd
from pathlib import Path

# Répertoires de base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ACTUAL_PATH = DATA_DIR / "actual_weather" / "actual_weather.csv"
HISTORICAL_PATH = DATA_DIR / "historical_weather" / "historical_weather.csv"
HISTORICAL_SUMMARY_PATH = DATA_DIR / "historical_weather" / "historical_summary.csv"
FORECAST_PATH = DATA_DIR / "forecast_weather" / "forecast_weather.csv"

def transform_actual():
    df = pd.read_csv(ACTUAL_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["date", "city"])
    df.to_csv(ACTUAL_PATH, index=False)
    print("✅ Transformed actual weather (overwritten)")

def transform_historical():
    df = pd.read_csv(HISTORICAL_PATH)
    df["time"] = pd.to_datetime(df["time"])
    df["annee"] = df["time"].dt.year
    df["mois"] = df["time"].dt.strftime("%B")

    mois_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    df["mois"] = pd.Categorical(df["mois"], categories=mois_order, ordered=True)

    df_resume = df.groupby(["ville", "annee", "mois"], observed=True).agg({
        "temperature_2m_mean (°C)": "mean",
        "temperature_2m_min (°C)": "mean",
        "temperature_2m_max (°C)": "mean",
        "relative_humidity_2m_mean (%)": "mean",
        "wind_speed_10m_mean (km/h)": "mean"
    }).reset_index()

    df_resume.columns = [
        "city", "year", "months",
        "average temperature", "min temperature", "max temperature",
        "humidity", "wind speed"
    ]

    df_resume[["average temperature", "min temperature", "max temperature", "humidity", "wind speed"]] = df_resume[
        ["average temperature", "min temperature", "max temperature", "humidity", "wind speed"]
    ].round(2)

    df_resume = df_resume.sort_values(by=["year", "months", "city"]).reset_index(drop=True)

    HISTORICAL_SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_resume.to_csv(HISTORICAL_SUMMARY_PATH, index=False)

    print("✅ Transformed and summarized historical weather saved to historical_summary.csv")

def transform_forecast():
    df = pd.read_csv(FORECAST_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by=["date", "city"])
    df.to_csv(FORECAST_PATH, index=False)
    print("✅ Transformed forecast weather (overwritten)")

def transform():
    transform_actual()
    transform_historical()
    transform_forecast()

if __name__ == "__main__":
    transform()
