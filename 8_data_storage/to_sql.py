# to_sql.py
# Store scraped data (quotes) into a SQL database using SQLAlchemy and pandas

import pandas as pd
from sqlalchemy import create_engine

# Use SQLite for local testing
# For PostgreSQL: "postgresql://user:password@host:port/dbname"
DATABASE_URL = "sqlite:///scraped_data.db"

def load_scraped_data(csv_path):
    return pd.read_csv(csv_path)

def store_to_sql(df, table_name="quotes", if_exists="append"):
    engine = create_engine(DATABASE_URL)
    df.to_sql(table_name, con=engine, index=False, if_exists=if_exists)
    print(f"[+] Inserted {len(df)} records into table '{table_name}'.")

def main():
    data = load_scraped_data("quotes_output.csv")
    store_to_sql(data)

if __name__ == "__main__":
    main()