import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🏠 Home Dashboard")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# Latest year selector
years = sorted(ratios["year"].unique())

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    years,
    index=len(years)-1
)

ratios = ratios[
    ratios["year"] == selected_year
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Companies",
    len(companies)
)

col2.metric(
    "Average ROE",
    round(
        ratios["return_on_equity_pct"].mean(),
        2
    )
)

col3.metric(
    "Median D/E",
    round(
        ratios["debt_to_equity"].median(),
        2
    )
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Median Revenue CAGR",
    #round(
        #ratios["asset_turnover"].median(),
        2
    )
#)

col5.metric(
    "Median P/E",
    #round(
       # ratios["interest_coverage"].median(),
        2
    )
#)

debt_free = len(
    ratios[
        ratios["debt_to_equity"] == 0
    ]
)

col6.metric(
    "Debt Free Companies",
    debt_free
)

st.divider()

st.subheader("Top 5 Companies by ROE")

top5 = ratios.sort_values(
    "return_on_equity_pct",
    ascending=False
).head(5)

st.dataframe(
    top5[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "net_profit_margin_pct"
        ]
    ],
    use_container_width=True
)

st.divider()

st.subheader("ROE Distribution")

fig = px.histogram(
    ratios,
    x="return_on_equity_pct",
    nbins=20
)

st.plotly_chart(
    fig,
    use_container_width=True
)