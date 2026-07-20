import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🏢 Company Profile")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ticker = st.selectbox(
    "Select Company",
    companies["id"].sort_values()
)

company = companies[
    companies["id"] == ticker
].iloc[0]

st.subheader(company["company_name"])

col1, col2 = st.columns(2)

with col1:

    st.write("### Company Information")

    st.write(
        f"**Ticker:** {company['id']}"
    )

    st.write(
        f"**Face Value:** {company['face_value']}"
    )

    st.write(
        f"**Book Value:** {company['book_value']}"
    )

    st.write(
        f"**ROCE:** {company['roce_percentage']}"
    )

    st.write(
        f"**ROE:** {company['roe_percentage']}"
    )

with col2:

    st.write("### About")

    st.write(
        company["about_company"]
    )

ratios = pd.read_sql(
    f"""
    SELECT *
    FROM financial_ratios
    WHERE company_id='{ticker}'
    """,
    conn
)

pl = pd.read_sql(
    f"""
    SELECT *
    FROM profitandloss
    WHERE company_id='{ticker}'
    """,
    conn
)

proscons = pd.read_sql(
    f"""
    SELECT *
    FROM prosandcons
    WHERE company_id='{ticker}'
    """,
    conn
)
conn.close()

latest = ratios.iloc[-1]

st.divider()

k1, k2, k3 = st.columns(3)

k1.metric(
    "ROE",
    latest["return_on_equity_pct"]
)

k2.metric(
    "Debt / Equity",
    latest["debt_to_equity"]
)

k3.metric(
    "Net Profit Margin",
    latest["net_profit_margin_pct"]
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "OPM",
    latest["operating_profit_margin_pct"]
)

k5.metric(
    "Interest Coverage",
    latest["interest_coverage"]
)

k6.metric(
    "Asset Turnover",
    latest["asset_turnover"]
)

st.divider()

if len(pl) > 0:

    fig = px.bar(
        pl,
        x="year",
        y="sales",
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

if len(ratios) > 0:

    fig2 = px.line(
        ratios,
        x="year",
        y=[
            "return_on_equity_pct",
            "net_profit_margin_pct"
        ],
        title="ROE & Net Profit Margin"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

st.subheader("✅ Pros & ❌ Cons")

if len(proscons) > 0:

    col1, col2 = st.columns(2)

    with col1:
        st.success("Pros")
        st.write(proscons.iloc[0]["pros"])

    with col2:
        st.error("Cons")
        st.write(proscons.iloc[0]["cons"])

else:

    st.info("No Pros & Cons available.")