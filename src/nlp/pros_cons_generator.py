import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

analysis = pd.read_sql("""
SELECT *
FROM analysis
""", conn)

conn.close()


latest = (
    ratios["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

ratios["year_num"] = latest

latest_year = ratios["year_num"].max()

ratios = ratios[
    (ratios["year_num"] == latest_year)
    &
    (ratios["year"].str.contains("Mar", na=False))
]

df = ratios.merge(
    analysis,
    on="company_id",
    how="left"
)

# Convert CAGR columns to numeric

df["compounded_sales_growth"] = pd.to_numeric(
    df["compounded_sales_growth"],
    errors="coerce"
)

df["compounded_profit_growth"] = pd.to_numeric(
    df["compounded_profit_growth"],
    errors="coerce"
)

records = []

for _, row in df.iterrows():

    company = row["company_id"]

    # ---------- PROS ----------

    if row["return_on_equity_pct"] >= 20:
        records.append([
            company,
            "Pro",
            "P1",
            "Consistently high ROE indicates efficient capital utilisation.",
            90
        ])

    if row["free_cash_flow_cr"] > 0:
        records.append([
            company,
            "Pro",
            "P2",
            "Positive Free Cash Flow reflects healthy business fundamentals.",
            85
        ])

    if row["debt_to_equity"] == 0:
        records.append([
            company,
            "Pro",
            "P3",
            "Debt-free balance sheet provides financial flexibility.",
            95
        ])

    if (
        pd.notna(row["compounded_sales_growth"])
        and
        row["compounded_sales_growth"] > 15
    ):
        records.append([
            company,
            "Pro",
            "P4",
            "Revenue CAGR above 15% reflects strong business growth.",
            88
        ])

    if row["operating_profit_margin_pct"] > 25:
        records.append([
            company,
            "Pro",
            "P5",
            "High operating margin indicates strong pricing power.",
            82
        ])

    # ---------- CONS ----------

    if row["debt_to_equity"] > 2:
        records.append([
            company,
            "Con",
            "C1",
            "High debt-to-equity ratio requires monitoring.",
            90
        ])

    if row["free_cash_flow_cr"] < 0:
        records.append([
            company,
            "Con",
            "C2",
            "Negative Free Cash Flow raises cash generation concerns.",
            88
        ])

    if row["interest_coverage"] < 1.5:
        records.append([
            company,
            "Con",
            "C3",
            "Low Interest Coverage indicates debt servicing risk.",
            85
        ])

    if row["dividend_payout_ratio_pct"] > 100:
        records.append([
            company,
            "Con",
            "C4",
            "Dividend payout above 100% may not be sustainable.",
            82
        ])

    if (
        pd.notna(row["compounded_sales_growth"])
        and
        row["compounded_sales_growth"] < 5
    ):
        records.append([
            company,
            "Con",
            "C5",
            "Low revenue growth indicates weak business momentum.",
            80
        ])

pros_cons = pd.DataFrame(
    records,
    columns=[
        "company_id",
        "type",
        "rule_id",
        "text",
        "confidence_pct"
    ]
)

pros_cons.to_csv(
    "output/pros_cons_generated.csv",
    index=False
)

print("Pros & Cons Generated Successfully")
print(pros_cons.head())
print("Total Rows:", len(pros_cons))