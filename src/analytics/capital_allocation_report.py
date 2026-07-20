import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

cash = pd.read_excel("output/cashflow_intelligence.xlsx")

conn.close()

# Remove duplicate companies
cash = cash.drop_duplicates(subset=["company_id"])

# Distribution
summary = (
    cash.groupby("capital_allocation_label")
    .size()
    .reset_index(name="company_count")
)

summary.to_csv(
    "output/capital_allocation_summary.csv",
    index=False
)

# Pattern Changes (placeholder)
changes = cash[
    ["company_id", "capital_allocation_label"]
].copy()

changes.rename(
    columns={
        "capital_allocation_label": "latest_pattern"
    },
    inplace=True
)

changes["previous_pattern"] = "Unknown"

changes.to_csv(
    "output/pattern_changes.csv",
    index=False
)

print(summary)
print()
print("Capital Allocation Report Completed")