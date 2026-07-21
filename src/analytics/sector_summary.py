import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

# Broad sector summary
sector_summary = pd.read_sql("""
SELECT
    broad_sector,
    COUNT(*) AS company_count,
    ROUND(AVG(index_weight_pct),2) AS avg_index_weight
FROM sectors
GROUP BY broad_sector
ORDER BY company_count DESC
""", conn)

# Market cap summary
market_cap_summary = pd.read_sql("""
SELECT
    market_cap_category,
    COUNT(*) AS company_count
FROM sectors
GROUP BY market_cap_category
ORDER BY company_count DESC
""", conn)

sector_summary.to_csv(
    "output/sector_summary.csv",
    index=False
)

market_cap_summary.to_csv(
    "output/market_cap_summary.csv",
    index=False
)

print("Sector Summary")
print(sector_summary)

print("\nMarket Cap Summary")
print(market_cap_summary)

conn.close()
print("\nSector Analytics Completed")