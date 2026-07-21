from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

import sqlite3
import pandas as pd
import os
import sys

# ---------------- Company ID ----------------

company_id = "ABB"

if len(sys.argv) > 1:
    company_id = sys.argv[1]

styles = getSampleStyleSheet()

os.makedirs("reports/tearsheets", exist_ok=True)

# ---------------- Database ----------------

conn = sqlite3.connect("db/nifty100.db")

company = pd.read_sql(f"""
SELECT *
FROM companies
WHERE id='{company_id}'
""", conn)

if company.empty:
    print(f"Company {company_id} not found")
    conn.close()
    sys.exit()

ratios = pd.read_sql(f"""
SELECT *
FROM financial_ratios
WHERE company_id='{company_id}'
ORDER BY year DESC
LIMIT 1
""", conn)

conn.close()

# ---------------- Missing Ratios ----------------

if ratios.empty:
    ratios = pd.DataFrame([{
        "debt_to_equity": "NA",
        "interest_coverage": "NA"
    }])

# ---------------- Pros & Cons ----------------

pros_df = pd.read_csv("output/pros_cons_generated.csv")

pros_df = pros_df[
    pros_df["company_id"] == company_id
]

pro_list = (
    pros_df[
        pros_df["type"] == "Pro"
    ]["text"]
    .drop_duplicates()
    .tolist()
)

con_list = (
    pros_df[
        pros_df["type"] == "Con"
    ]["text"]
    .drop_duplicates()
    .tolist()
)

if len(pro_list) == 0:
    pro_list = ["No Pros Available"]

if len(con_list) == 0:
    con_list = ["No Cons Available"]

# ---------------- PDF ----------------

doc = SimpleDocTemplate(
    f"reports/tearsheets/{company_id}_tearsheet.pdf",
    pagesize=A4
)

elements = []

# ---------------- Title ----------------

elements.append(
    Paragraph(
        f"<b>{company.iloc[0]['company_name']}</b>",
        styles["Title"]
    )
)

elements.append(Spacer(1,20))

# ---------------- KPI Table ----------------

kpi = [

    ["ROE", company.iloc[0]["roe_percentage"]],
    ["ROCE", company.iloc[0]["roce_percentage"]],
    ["Book Value", company.iloc[0]["book_value"]],
    ["Face Value", company.iloc[0]["face_value"]],

    ["Debt / Equity",
     ratios.iloc[0]["debt_to_equity"]],

    ["Interest Coverage",
     ratios.iloc[0]["interest_coverage"]]

]

table = Table(kpi)

table.setStyle(TableStyle([

    ("GRID",(0,0),(-1,-1),1,colors.black),

    ("BACKGROUND",(0,0),(-1,0),colors.lightblue),

    ("BOTTOMPADDING",(0,0),(-1,-1),8),

]))

elements.append(table)

elements.append(Spacer(1,20))

# ---------------- Pros ----------------

elements.append(
    Paragraph(
        "<b>Pros</b>",
        styles["Heading2"]
    )
)

for p in pro_list:

    elements.append(
        Paragraph(
            "• " + str(p),
            styles["BodyText"]
        )
    )

elements.append(Spacer(1,20))

# ---------------- Cons ----------------

elements.append(
    Paragraph(
        "<b>Cons</b>",
        styles["Heading2"]
    )
)

for c in con_list:

    elements.append(
        Paragraph(
            "• " + str(c),
            styles["BodyText"]
        )
    )

# ---------------- Build ----------------

doc.build(elements)

print(f"PDF Generated Successfully : {company_id}")