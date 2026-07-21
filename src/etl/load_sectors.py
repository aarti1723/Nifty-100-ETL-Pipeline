import sqlite3
import pandas as pd

# Read Excel
df = pd.read_excel("data/sectors.xlsx")

# Connect DB
conn = sqlite3.connect("db/nifty100.db")

# Load into SQLite
df.to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

print("Sectors Loaded Successfully")
print(df.head())
print("Rows:", len(df))