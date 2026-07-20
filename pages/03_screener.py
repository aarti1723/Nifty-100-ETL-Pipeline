import streamlit as st
import sqlite3
import pandas as pd

st.title("🔍 Stock Screener")

# ----------------------------
# Load Data
# ----------------------------
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

# ----------------------------
# Latest Year Filter
# ----------------------------

import re

# Extract year number from strings like "Mar 2024"
ratios["year_num"] = (
    ratios["year"]
    .str.extract(r'(\d{4})')
    .astype(float)
)

latest = ratios["year_num"].max()

ratios = ratios[
    (ratios["year_num"] == latest)
    &
    (ratios["year"].str.contains("Mar", na=False))
]

# ----------------------------
# Merge Tables
# ----------------------------
filtered_data = ratios.merge(
    analysis,
    on="company_id",
    how="left"
)

st.write("Rows after merge:", len(filtered_data))
import re

def extract_5yr(value):
    if pd.isna(value):
        return None

    value = str(value)

    if "5 Years" in value:
        match = re.search(r"(\d+(\.\d+)?)%", value)
        if match:
            return float(match.group(1))

    return None



# ----------------------------
# Convert Numeric Columns
# ----------------------------
numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "sales_growth_5yr",
    "profit_growth_5yr"
]
filtered_data["sales_growth_5yr"] = pd.to_numeric(
    filtered_data["compounded_sales_growth"],
    errors="coerce"
)

filtered_data["profit_growth_5yr"] = pd.to_numeric(
    filtered_data["compounded_profit_growth"],
    errors="coerce"
)
st.write(filtered_data.head(10))

st.write(
    filtered_data[
        [
            "company_id",
            "compounded_sales_growth",
            "sales_growth_5yr",
            "compounded_profit_growth",
            "profit_growth_5yr"
        ]
    ].head(10)
)

for col in numeric_cols:
    if col in filtered_data.columns:
        filtered_data[col] = pd.to_numeric(
            filtered_data[col],
            errors="coerce"
        )

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    0,
    50,
    15
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    1.0
)

opm = st.sidebar.slider(
    "Minimum OPM",
    0,
    50,
    10
)

sales_growth = st.sidebar.slider(
    "Minimum Sales Growth",
    0,
    50,
    10
)

profit_growth = st.sidebar.slider(
    "Minimum Profit Growth",
    0,
    50,
    10
)

# ----------------------------
# Apply Filters
# ----------------------------
st.write("Total rows:", len(filtered_data))

st.write(filtered_data[
    [
        "company_id",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "sales_growth_5yr",
        "profit_growth_5yr"
    ]
].head(20))
st.write(filtered_data[
    [
        "sales_growth_5yr",
        "profit_growth_5yr"
    ]
].describe())

filtered = filtered_data[
    (filtered_data["return_on_equity_pct"] >= roe)
    &
    (filtered_data["debt_to_equity"] <= de)
    &
    (filtered_data["operating_profit_margin_pct"] >= opm)
    &
    (filtered_data["sales_growth_5yr"] >= sales_growth)
    &
    (filtered_data["profit_growth_5yr"] >= profit_growth)
]

# ----------------------------
# Output
# ----------------------------
st.success(f"{len(filtered)} companies match your filters")

st.dataframe(
    filtered[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "operating_profit_margin_pct",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "sales_growth_5yr",
            "profit_growth_5yr",
        ]
    ],
    width="stretch"
)
st.write(filtered_data[[
    "company_id",
    "sales_growth_5yr",
    "profit_growth_5yr"
]].head(20))
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    csv,
    "screener.csv",
    "text/csv"
)