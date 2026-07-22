# Nifty100 ETL Pipeline – Analyst Guide

## Overview
This project provides financial analytics for Nifty100 companies using an ETL pipeline, SQLite database, Streamlit dashboard, clustering analysis, and FastAPI.

---

## Database

Database: db/nifty100.db

Main Tables

- companies
- financial_ratios
- balancesheet
- cashflow
- profitandloss
- analysis
- sectors
- stock_prices
- market_cap
- peer_groups
- peer_percentiles
- documents
- prosandcons

---

## Dashboard

Run

streamlit run app.py

Dashboard includes

- Company Search
- Financial Ratios
- Balance Sheet
- Cashflow
- Profit & Loss
- Peer Comparison
- Sector Analysis
- Valuation Summary

---

## FastAPI

Run

python -m uvicorn src.api.main:app --reload

Swagger

http://127.0.0.1:8000/docs

API includes

- Companies
- Financial Ratios
- Analysis
- Cashflow
- Balance Sheet
- Profit & Loss
- Sector
- Documents
- Pros & Cons
- Peer Groups
- Peer Percentiles
- Market Cap
- Stock Prices

---

## Analytics

Implemented

- Financial Ratio Analysis
- Company Clustering
- Cashflow Intelligence
- Capital Allocation
- Sector Reports

---

## Reports Generated

output/

- cluster_labels.csv
- cluster_summary.csv
- cashflow_intelligence.xlsx
- valuation_summary.xlsx
- screener_output.xlsx
- peer_comparison.xlsx

reports/

- pytest_report.html
- elbow_plot.png

---

## Testing

Run

python -m pytest

Result

73 Tests Passed

---

## Author

Aarti Kumari