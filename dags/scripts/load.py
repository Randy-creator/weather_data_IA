import os
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import json
import tempfile

GOOGLE_SHEET_NAME = "weatherData"

# Répertoire de base
BASE_DIR = Path(__file__).resolve().parent.parent

# Fichiers CSV à charger (y compris le fichier résumé transformé pour l'historique)
CSV_FILES = {
    "actual_weather": BASE_DIR / "data" / "actual_weather" / "actual_weather.csv",
    "forecast_weather": BASE_DIR / "data" / "forecast_weather" / "forecast_weather.csv",
    "historic_weather": BASE_DIR / "data" / "historical_weather" / "historical_summary.csv",  # ✅ correction ici
}

def load_csv_to_gsheet(csv_path, sheet_name, worksheet_name):
    print(f"📤 Loading {csv_path} to tab: '{worksheet_name}' in sheet: '{sheet_name}'...")

    credentials_str = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not credentials_str:
        raise EnvironmentError("❌ GOOGLE_CREDENTIALS_JSON environment variable not set.")

    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp_file:
        tmp_file.write(credentials_str)
        tmp_file_path = tmp_file.name

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(tmp_file_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name)

    try:
        worksheet = sheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        print(f"🆕 Worksheet '{worksheet_name}' not found. Creating it.")
        worksheet = sheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

    df = pd.read_csv(csv_path)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(f"✅ Data replaced in tab: '{worksheet_name}'.")

def load():
    for worksheet_name, csv_path in CSV_FILES.items():
        load_csv_to_gsheet(csv_path, GOOGLE_SHEET_NAME, worksheet_name)

if __name__ == "__main__":
    load()
