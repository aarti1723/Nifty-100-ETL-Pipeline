import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
sectors = pd.read_sql("SELECT company_id,broad_sector FROM sectors", conn)

conn.close()

ratios["year_num"] = (
    ratios["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

latest = ratios["year_num"].max()

ratios = ratios[
    (ratios["year_num"] == latest)
    &
    (ratios["year"].str.contains("Mar", na=False))
]

df = ratios.merge(
    sectors,
    on="company_id",
    how="left"
)

# ================= FUNCTIONS =================

def free_cash_flow(cfo, cfi):
    return cfo + cfi


def cfo_quality_score(cfo, pat):
    if pat == 0:
        return None

    score = cfo / pat

    if score > 1:
        return "High Quality"
    elif score >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    if sales == 0:
        return None

    return abs(investing_activity) / sales * 100


def fcf_conversion(fcf, operating_profit):
    if operating_profit == 0:
        return None

    return fcf / operating_profit * 100

# ---------- Calculate KPIs ----------

df["fcf"] = df.apply(
    lambda x: free_cash_flow(
        x["cash_from_operations_cr"],
        x["capex_cr"]
    ),
    axis=1
)

df["cfo_quality_label"] = df.apply(
    lambda x: cfo_quality_score(
        x["cash_from_operations_cr"],
        x["free_cash_flow_cr"]
    ),
    axis=1
)

df["capex_intensity_pct"] = df.apply(
    lambda x: capex_intensity(
        x["capex_cr"],
        abs(x["cash_from_operations_cr"])
    ),
    axis=1
)

df["fcf_conversion_pct"] = df.apply(
    lambda x: fcf_conversion(
        x["fcf"],
        x["cash_from_operations_cr"]
    ),
    axis=1
)

df["distress_flag"] = df["cash_from_operations_cr"].apply(
    lambda x: "YES" if x < 0 else "NO"
)

df["deleveraging_flag"] = df["debt_to_equity"].apply(
    lambda x: "YES" if x < 1 else "NO"
)

def capital(row):
    if row["fcf"] > 0 and row["capex_cr"] < 0:
        return "Reinvestor"
    elif row["fcf"] > 0:
        return "Cash Generator"
    else:
        return "Distress Signal"

df["capital_allocation_label"] = df.apply(capital, axis=1)

output = df[
    [
        "company_id",
        "broad_sector",
        "cfo_quality_label",
        "capex_intensity_pct",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label"
    ]
]

output.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

output[
    output["distress_flag"] == "YES"
].to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("Cashflow Intelligence Completed")
print(output.head())
print("Rows:", len(output))