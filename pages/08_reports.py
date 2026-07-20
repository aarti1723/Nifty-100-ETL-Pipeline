import streamlit as st
import sqlite3
import pandas as pd

st.title("📄 Annual Reports")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("""
SELECT
    id,
    company_name
FROM companies
ORDER BY company_name
""", conn)

documents = pd.read_sql("""
SELECT *
FROM documents
""", conn)

conn.close()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

reports = documents[
    documents["company_id"] == company_id
]

if reports.empty:
    st.warning("No reports available.")
else:

    st.subheader(company)

    reports = reports.sort_values("year", ascending=False)

    st.dataframe(
    reports[
        [
            "year",
            "annual_report"
        ]
    ],
    use_container_width=True
)

st.subheader("Available Reports")

for _, row in reports.iterrows():

    st.markdown(
        f"### {row['year']}"
    )

    st.markdown(
        f"[📄 Open Annual Report]({row['annual_report']})"
    )

    st.markdown("---")