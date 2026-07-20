import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🗺️ Capital Allocation Map")

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql("""
SELECT
company_id,
free_cash_flow_cr,
debt_to_equity,
return_on_equity_pct
FROM financial_ratios
""", conn)

companies = pd.read_sql("""
SELECT
id,
company_name
FROM companies
""", conn)

conn.close()

# Latest data only
ratios = ratios.drop_duplicates(subset="company_id", keep="last")

df = ratios.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

def classify(row):

    if row["free_cash_flow_cr"] > 0 and row["debt_to_equity"] < 0.5:
        return "Debt Free Compounders"

    elif row["free_cash_flow_cr"] > 0:
        return "Cash Generators"

    elif row["debt_to_equity"] > 2:
        return "Highly Leveraged"

    elif row["return_on_equity_pct"] > 20:
        return "High ROE"

    else:
        return "Others"

df["capital_pattern"] = df.apply(classify, axis=1)

df["size"] = 1

st.write(df["capital_pattern"].value_counts())
st.write(df.head())

fig = px.treemap(
    df,
    path=["capital_pattern", "company_name"],
    values="size",
    color="capital_pattern",
    title="Capital Allocation Map"
)
st.plotly_chart(fig, use_container_width=True)

pattern = st.selectbox(
    "Select Pattern",
    sorted(df["capital_pattern"].unique())
)

st.dataframe(
    df[df["capital_pattern"]==pattern][
        [
            "company_id",
            "company_name",
            "return_on_equity_pct",
            "free_cash_flow_cr",
            "debt_to_equity"
        ]
    ],
    use_container_width=True
)