"""
Run all queries in queries.sql and print results.
Handles SQL comments correctly.
"""
import sqlite3
import re

conn = sqlite3.connect("data/nepal_agriculture.db")
cursor = conn.cursor()

with open("queries.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# Step 1: Remove full-line comment lines (starting with --)
lines = [line for line in sql.split("\n") if not line.strip().startswith("--")]
sql_clean = "\n".join(lines)

# Step 2: Split into individual queries on semicolons
queries = [q.strip() for q in sql_clean.split(";") if q.strip()]

print(f"Found {len(queries)} queries\n")

# Step 3: Run each query and print results
for i, q in enumerate(queries, 1):
    print("=" * 70)
    print(f"QUERY {i}")
    print("=" * 70)

    try:
        cursor.execute(q)
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()

        # Print header
        print(" | ".join(cols))
        print("-" * 70)

        # Print rows
        for row in rows:
            print(" | ".join(str(v) for v in row))

        print(f"\n({len(rows)} rows)\n")

    except Exception as e:
        print(f"ERROR: {e}\n")

conn.close()