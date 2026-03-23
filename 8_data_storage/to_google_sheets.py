# to_google_sheets.py
# Push data from CSV to a Google Sheet using Service Account

import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

CSV_FILE = "quotes_output.csv"
GOOGLE_SHEET_NAME = "ScrapedQuotes"
WORKSHEET_NAME = "Quotes"

def get_gsheet_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("google_credentials.json", scope)
    client = gspread.authorize(creds)
    return client

def upload_to_sheet(csv_path):
    df = pd.read_csv(csv_path)
    client = get_gsheet_client()

    sheet = client.open(GOOGLE_SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME)

    worksheet.clear()
    set_with_dataframe(worksheet, df)
    print(f"[+] Uploaded {len(df)} rows to Google Sheet → {GOOGLE_SHEET_NAME}/{WORKSHEET_NAME}")

def main():
    upload_to_sheet(CSV_FILE)

if __name__ == "__main__":
    main()