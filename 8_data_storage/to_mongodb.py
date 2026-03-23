# to_mongodb.py
# Load scraped data and insert into MongoDB

import pandas as pd
from pymongo import MongoClient, errors

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "scraping_demo"
COLLECTION_NAME = "quotes"

def load_data(csv_path):
    return pd.read_csv(csv_path).to_dict(orient="records")

def store_to_mongo(records):
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        result = collection.insert_many(records)
        print(f"[+] Inserted {len(result.inserted_ids)} documents into MongoDB.")
    except errors.BulkWriteError as bwe:
        print("[!] Bulk write error:", bwe.details)

def main():
    records = load_data("quotes_output.csv")
    store_to_mongo(records)

if __name__ == "__main__":
    main()