"""
Build a SQLite database from the cleaned crop + rainfall data.
Run this once to create nepal_agriculture.db
"""
import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = "data/nepal_agriculture.db"

# Remove existing DB so we start fresh
if Path(DB_PATH).exists():
    Path(DB_PATH).unlink()
    print(f"Removed existing {DB_PATH}")

# Load cleaned data
merged = pd.read_csv("data/merged_data.csv")
rain = pd.read_csv("data/rainfall_yearly.csv")

print(f"Loaded merged: {merged.shape}")
print(f"Loaded rainfall: {rain.shape}")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)

# Write tables
merged.to_sql("crop_yields", conn, if_exists="replace", index=False)
rain.to_sql("rainfall_yearly", conn, if_exists="replace", index=False)

conn.commit()

# Verify
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTables created: {[t[0] for t in tables]}")

for table in ["crop_yields", "rainfall_yearly"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count} rows")

conn.close()
print(f"\n✅ Database ready: {DB_PATH}")