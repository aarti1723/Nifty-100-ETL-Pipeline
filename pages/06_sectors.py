import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("📊 Sector Analysis")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
sectors = pd.read_sql("SELECT * FROM sectors", conn)
ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
market = pd.read_sql("SELECT * FROM market_cap", conn)

conn.close()

# ---------------- Latest Year ----------------

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

market = market[
    market["year"] == market["year"].max()
]

# ---------------- Merge ----------------

# Keep only required columns
companies = companies[["id", "company_name"]]

sectors = sectors[
    [
        "company_id",
        "broad_sector",
        "sub_sector"
    ]
]

ratios = ratios[
    [
        "company_id",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity"
    ]
]

market = market[
    [
        "company_id",
        "market_cap_crore"
    ]
]

# Merge
df = sectors.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.merge(
    ratios,
    on="company_id",
    how="left"
)

df = df.merge(
    market,
    on="company_id",
    how="left"
)
# ---------------- Sector Dropdown ----------------

sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].dropna().unique())
)

sector_df = df[df["broad_sector"] == sector]

sector_df = sector_df.dropna(
    subset=[
        "market_cap_crore",
        "return_on_equity_pct"
    ]
)

# ---------------- Bubble Chart ----------------

fig = px.scatter(
    sector_df,
    x="market_cap_crore",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    title=f"{sector} Companies",
    labels={
        "market_cap_crore":"Market Cap (₹ Cr)",
        "return_on_equity_pct":"ROE %"
    }
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Median KPI ----------------

median = pd.DataFrame({
    "Metric":[
        "ROE",
        "Net Margin",
        "OPM",
        "Debt/Equity"
    ],
    "Value":[
        sector_df["return_on_equity_pct"].median(),
        sector_df["net_profit_margin_pct"].median(),
        sector_df["operating_profit_margin_pct"].median(),
        sector_df["debt_to_equity"].median()
    ]
})

fig2 = px.bar(
    median,
    x="Metric",
    y="Value",
    color="Metric",
    title="Sector Median KPIs"
)

st.plotly_chart(fig2, use_container_width=True)