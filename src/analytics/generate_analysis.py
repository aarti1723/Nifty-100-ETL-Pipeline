import pandas as pd
import re
from cagr import revenue_cagr, pat_cagr

# ----------------------------
# Load Profit & Loss
# ----------------------------
pl = pd.read_excel(
    "data/profitandloss.xlsx",
    header=1
)

# ----------------------------
# Clean Year
# ----------------------------
def clean_year(value):
    value = str(value)

    if value == "TTM":
        return 9999

    match = re.search(r'(\d{4})', value)

    if match:
        return int(match.group(1))

    return None


pl["year_num"] = pl["year"].apply(clean_year)

companies = sorted(pl["company_id"].unique())

analysis_rows = []

print(f"Companies found : {len(companies)}")

for company in companies:

    temp = (
        pl[
            (pl["company_id"] == company)
            &
            (pl["year_num"] != 9999)
        ]
        .sort_values("year_num")
    )

    if len(temp) < 6:
        continue

    start = temp.iloc[-6]
    end = temp.iloc[-1]

    years = end["year_num"] - start["year_num"]

    sales_cagr = revenue_cagr(
        start["sales"],
        end["sales"],
        years
    )

    profit_cagr = pat_cagr(
        start["net_profit"],
        end["net_profit"],
        years
    )

    analysis_rows.append({
        "company_id": company,
        "compounded_sales_growth": round(sales_cagr, 2) if sales_cagr else None,
        "compounded_profit_growth": round(profit_cagr, 2) if profit_cagr else None
    })

analysis = pd.DataFrame(analysis_rows)

analysis.to_excel(
    "data/analysis.xlsx",
    index=False
)

print(analysis.head())

print(f"\nGenerated analysis for {len(analysis)} companies.")