# NIFTY100 ETL & Financial Analytics Dashboard

## Overview

This project is a complete Financial Analytics platform for NIFTY 100 companies built using **Python, Pandas, SQLite, Plotly and Streamlit**.

The project covers:

- ETL Pipeline
- Database Design
- Financial Ratio Analysis
- CAGR Analysis
- Peer Comparison
- Stock Screener
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Reports
- Valuation Module

---

# Tech Stack

- Python
- SQLite
- Pandas
- NumPy
- Plotly
- Streamlit
- OpenPyXL
- Pytest

---

# Project Structure

```
Nifty-100-ETL-Pipeline
│
├── app.py
├── db/
├── data/
├── output/
├── pages/
│   ├── 01_home.py
│   ├── 02_profile.py
│   ├── 03_screener.py
│   ├── 04_peers.py
│   ├── 05_trends.py
│   ├── 06_sectors.py
│   ├── 07_capital.py
│   └── 08_reports.py
│
├── src/
│   ├── analytics/
│   └── dashboard/
│
└── README.md
```

---

# Dashboard

Run the application:

```bash
streamlit run app.py
```

Dashboard URL:

```
http://localhost:8501
```

---

# Dashboard Features

## Home

- Market KPIs
- Sector Distribution
- Top Quality Companies

## Company Profile

- Company Search
- Revenue Trend
- Profit Trend
- ROE Analysis
- Financial KPIs
- Pros & Cons

## Stock Screener

- Growth Filters
- Profitability Filters
- Debt Filters
- CSV Download

## Peer Comparison

- Peer Group Comparison
- KPI Comparison Table

## Trend Analysis

- Revenue Trend
- Profit Trend
- Cash Flow Trend

## Sector Analysis

- Bubble Chart
- Sector Median KPIs

## Capital Allocation Map

- Treemap Visualization
- Capital Allocation Categories

## Annual Reports

- Company-wise Annual Reports
- Direct Report Links

---

# Valuation Module

Calculates

- Free Cash Flow Yield
- Sector Median PE
- Discount Flag
- Fair Value Flag
- Caution Flag

Generated Outputs

```
output/valuation_summary.xlsx
output/valuation_flags.csv
```

---

# ETL Pipeline

The ETL pipeline performs

- Database Creation
- Data Loading
- Data Validation
- Data Cleaning
- Normalization
- Audit Report Generation

Generated Outputs

- load_audit.csv
- validation_failures.csv

---

# Data Quality Rules

Implemented DQ01 – DQ16

- Primary Key Validation
- Foreign Key Validation
- Duplicate Detection
- Company-Year Validation
- Balance Sheet Validation
- Financial Ratio Validation
- Positive Sales Validation
- OPM Validation

---

# Testing

Run

```bash
python -m pytest tests -v
```

All automated tests pass successfully.

---

# Sprint Progress

## Sprint 1

- Database Design
- ETL Pipeline
- Data Validation

## Sprint 2

- Financial Ratio Processing
- Data Cleaning
- SQLite Integration

## Sprint 3

- Financial Analytics
- CAGR Analysis
- Peer Groups
- Composite Quality Score
- Peer Percentiles

## Sprint 4

- Streamlit Dashboard
- Stock Screener
- Trend Analysis
- Sector Analysis
- Capital Allocation Map
- Annual Reports
- Valuation Module

---

# Author

**Aarti Kumari**

B.Tech Computer Science Engineering

Data Analytics | Python | SQL | Streamlit | Financial Analytics
