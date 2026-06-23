import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios",
    "peer_groups"
]

data = []

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    data.append([table, count])

conn.close()

audit = pd.DataFrame(
    data,
    columns=["table_name", "row_count"]
)

audit.to_csv(
    "output/load_audit.csv",
    index=False
)

print("load_audit.csv created successfully!")