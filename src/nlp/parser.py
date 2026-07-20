import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

analysis = pd.read_sql("SELECT * FROM analysis", conn)

conn.close()

records = []

for _, row in analysis.iterrows():

    company = row["company_id"]

    if pd.notna(row["compounded_sales_growth"]):
        records.append({
            "company_id": company,
            "metric_type": "Sales CAGR",
            "period_years": 5,
            "value_pct": float(row["compounded_sales_growth"])
        })

    if pd.notna(row["compounded_profit_growth"]):
        records.append({
            "company_id": company,
            "metric_type": "Profit CAGR",
            "period_years": 5,
            "value_pct": float(row["compounded_profit_growth"])
        })

parsed = pd.DataFrame(records)

parsed.to_csv(
    "output/analysis_parsed.csv",
    index=False
)

print("Parser Completed")
print(parsed.head())
print("Rows:", len(parsed))