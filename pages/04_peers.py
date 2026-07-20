import plotly.graph_objects as go
import streamlit as st
import sqlite3
import pandas as pd

st.title("👥 Peer Comparison")

conn = sqlite3.connect("db/nifty100.db")

# Latest financial ratios
ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

peers = pd.read_sql("""
SELECT *
FROM peer_groups
""", conn)

companies = pd.read_sql("""
SELECT id, company_name
FROM companies
""", conn)

conn.close()

# ---------- Latest March data ----------
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

# ---------- Company Selection ----------
company = st.selectbox(
    "Select Company",
    sorted(peers["company_id"].unique())
)

# ---------- Peer Group ----------
peer_group = peers.loc[
    peers["company_id"] == company,
    "peer_group_name"
].iloc[0]

st.subheader(f"Peer Group : {peer_group}")

peer_ids = peers[
    peers["peer_group_name"] == peer_group
]["company_id"]

comparison = ratios[
    ratios["company_id"].isin(peer_ids)
]

comparison = comparison.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)
comparison = comparison.merge(
    peers[["company_id", "is_benchmark"]],
    on="company_id",
    how="left"
)


comparison = comparison[
    [
        "company_id",
        "company_name",
        "is_benchmark",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr"
    ]
]
def highlight_benchmark(row):
    if row["is_benchmark"] == 1:
        return ["background-color: lightgreen"] * len(row)
    return [""] * len(row)

st.dataframe(
    comparison.style.apply(highlight_benchmark, axis=1),
    width="stretch"
)

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "interest_coverage",
    "asset_turnover",
    "debt_to_equity"
]

company_values = comparison[
    comparison["company_id"] == company
][metrics].iloc[0]

peer_avg = comparison[metrics].mean()

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=company_values.values,
    theta=[
        "ROE",
        "Net Margin",
        "OPM",
        "ICR",
        "Asset Turnover",
        "Debt/Equity"
    ],
    fill="toself",
    name=company
))

fig.add_trace(go.Scatterpolar(
    r=peer_avg.values,
    theta=[
        "ROE",
        "Net Margin",
        "OPM",
        "ICR",
        "Asset Turnover",
        "Debt/Equity"
    ],
    fill="toself",
    name="Peer Average"
))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True,
    height=600
)

st.plotly_chart(fig, use_container_width=True)