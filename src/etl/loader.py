import pandas as pd
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

files = {
"companies": ("companies.xlsx", 1),
"profitandloss": ("profitandloss.xlsx", 1),
"balancesheet": ("balancesheet.xlsx", 1),
"cashflow": ("cashflow.xlsx", 1),
"analysis": ("analysis.xlsx", 1),
"documents": ("documents.xlsx", 1),
"prosandcons": ("prosandcons.xlsx", 1),
"sectors": ("sectors.xlsx", 0),
"stock_prices": ("stock_prices.xlsx", 0),
"financial_ratios": ("financial_ratios.xlsx", 0),
"peer_groups": ("peer_groups.xlsx", 0)
}
companies_df = pd.read_excel(
    "data/companies.xlsx",
    header=1
)

valid_ids = set(companies_df["id"])

for table, (file, header_row) in files.items():
    print(f"\nLoading {table}...")
    df = pd.read_excel(
        f"data/{file}",
        header=header_row
    )
    if table == "stock_prices":
        df = df.rename(columns={
            "date": "price_date",
            "open_price": "open",
            "high_price": "high",
            "low_price": "low",
            "close_price": "close"
            })
    if "company_id" in df.columns:
        before = len(df)
        df = df[df["company_id"].isin(valid_ids)]
        removed = before - len(df)
        if removed:
            print(f"{table}: removed {removed} FK-invalid rows")
    df.to_sql(
        table,
        conn,
        if_exists="append",
        index=False
    )
    
    print(f"{table}: {len(df)} rows loaded")

conn.commit()
conn.close()

print("\nAll tables loaded successfully!")
