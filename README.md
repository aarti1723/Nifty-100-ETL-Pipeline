\# NIFTY100 ETL Data Engineering Project



\## Overview



This project implements an ETL pipeline for NIFTY100 financial data using Python, Pandas, and SQLite.



Sprint 1 focuses on:



\* Database creation

\* Data loading from Excel files

\* Data normalization

\* Data quality validation

\* Audit reporting

\* Unit testing



\## Project Structure



\* data/

\* db/

\* src/etl/

\* tests/etl/

\* notebooks/

\* output/



\## Deliverables



\* nifty100.db

\* load\_audit.csv

\* validation\_failures.csv

\* schema.sql

\* loader.py

\* validator.py

\* normaliser.py

\* exploratory\_queries.sql



\## Data Quality Rules



Implemented DQ01–DQ16 including:



\* Primary Key Validation

\* Foreign Key Validation

\* Company-Year Uniqueness

\* Balance Sheet Validation

\* OPM Validation

\* Positive Sales Validation

\* Financial Ratio Validation



\## Testing



Run:



python -m pytest tests/etl -v



Result:



39 tests passed



\## Exit Criteria



\* Companies Count = 92

\* Foreign Key Check Passed

\* Audit Report Generated

\* Validation Report Generated

\* 39 Unit Tests Passed



\## Author



Aarti Kumari



