import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("📈 Trend Analysis")

conn = sqlite3.connect("db/nifty100.db")

pl = pd.read_sql("""
SELECT company_id,
       year,
       sales,
       net_profit
FROM profitandloss
""", conn)

ratios = pd.read_sql("""
SELECT company_id,
       year,
       return_on_equity_pct
FROM financial_ratios
""", conn)

conn.close()

companies = sorted(pl["company_id"].unique())

company = st.selectbox(
    "Select Company",
    companies
)

pl = pl[
    (pl["company_id"] == company)
    &
    (~pl["year"].str.contains("TTM", na=False))
]

fig1 = px.line(
    pl,
    x="year",
    y="sales",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.line(
    pl,
    x="year",
    y="net_profit",
    markers=True,
    title="Net Profit Trend"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

roe = ratios[
    ratios["company_id"] == company
]

fig3 = px.line(
    roe,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="ROE Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)