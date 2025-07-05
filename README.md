    # Weather Comparison Project

This project compares historical, actual, and forecast weather data for the following cities:

- Paris  
- Tokyo  
- Nairobi  
- New York  
- Antananarivo  
- Sydney  

It uses three types of data:
- **Historical** data from Excel files
- **Actual** data from the OpenWeather API
- **Forecast** data (5-day forecast) from the OpenWeather API

---

## Goal

Allow comparison of climate trends across cities and time periods:

- Monthly temperature averages over years
- Current weather status per city
- Short-term (5-day) forecast per city

---

## Data Overview

| Dataset              | Columns                                                                                         |
|----------------------|--------------------------------------------------------------------------------------------------|
| `historical_summary.csv` | `city`, `year`, `months`, `average temperature`, `min temperature`, `max temperature`, `humidity`, `wind speed` |
| `actual_weather.csv`     | `city`, `date`, `average temperature`, `min temperature`, `max temperature`, `humidity`, `pressure`, `wind speed`, `description` |
| `forecast_weather.csv`   | `city`, `date`, `average temperature`, `min temperature`, `max temperature`, `humidity`, `pressure`, `wind speed`, `description` |

---

## Analysis Summary

### Historical Weather

- Time range: spans several years depending on city
- Aggregated by city, year, and month
- Use cases:
  - Compare seasonal temperatures
  - Identify cities with high wind or humidity
  - Analyze long-term climate patterns

### Actual Weather

- Current snapshot per city
- Use cases:
  - Compare northern and southern hemisphere differences
  - View present conditions (temperature, humidity, etc.)

### Forecast Weather

- Short-term future (5-day) average per city
- Use cases:
  - Trip planning
  - Observing upcoming changes in weather

---

Workflow:
1. `extract.py`: gets data from Excel and API
2. `transform.py`: cleans and formats the data
3. `load.py`: uploads it to Google Sheets

---

## Setup Instructions

### 1. Historical Files

Put your `.xlsx` files in `historical_source/` with filenames like:

- `paris_historic.xlsx`
- `nairobi_historic.xlsx`

Each file should contain consistent weather columns and a `time` column.

---

### 2. OpenWeather API Key

Update `extract.py`:

```python
API_KEY = "your_api_key_here"
```

### 3. Google Sheets Credentials
Create a service account in Google Cloud and export credentials.

Set your environment variable:
```
export GOOGLE_CREDENTIALS_JSON='{"type": "...", "project_id": "...", ...}'
```


# REQUIRES DEPENDENCIES:
```
pip install pandas requests gspread oauth2client openpyxl atplotlib seaborn notebook
```
