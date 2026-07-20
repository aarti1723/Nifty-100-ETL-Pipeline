import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

market = pd.read_sql("""
SELECT *
FROM market_cap
""", conn)

ratios = pd.read_sql("""
SELECT
company_id,
free_cash_flow_cr
FROM financial_ratios
""", conn)

sectors = pd.read_sql("""
SELECT
company_id,
broad_sector
FROM sectors
""", conn)

conn.close()

# Latest Market Cap
market = market.sort_values("year")
market = market.drop_duplicates("company_id", keep="last")

# Latest Ratios
ratios = ratios.drop_duplicates("company_id", keep="last")

df = market.merge(
    ratios,
    on="company_id",
    how="left"
)

df = df.merge(
    sectors,
    on="company_id",
    how="left"
)

# FCF Yield
df["FCF_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# Sector Median PE
sector_pe = (
    df.groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio":"sector_median_pe"
    },
    inplace=True
)

df = df.merge(
    sector_pe,
    on="broad_sector"
)

# Valuation Flag
def flag(row):

    if pd.isna(row["pe_ratio"]):
        return "Unknown"

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    if row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    return "Fair"

df["flag"] = df.apply(flag, axis=1)

summary = df[
    [
        "company_id",
        "broad_sector",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "sector_median_pe",
        "flag"
    ]
]

summary.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

summary[
    summary["flag"]!="Fair"
].to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("Valuation Module Completed")
print(summary.head())