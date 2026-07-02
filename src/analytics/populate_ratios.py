import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage,
    asset_turnover
)

# Read source files
pl = pd.read_excel("data/profitandloss.xlsx", header=1)
bs = pd.read_excel("data/balancesheet.xlsx", header=1)

# Merge P&L and Balance Sheet
df = pd.merge(
    pl,
    bs,
    on=["company_id", "year"],
    how="inner"
)

# -------------------------
# Ratio Calculations
# -------------------------

df["net_profit_margin_pct"] = df.apply(
    lambda x: net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

df["operating_profit_margin_pct"] = df.apply(
    lambda x: operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

df["return_on_equity_pct"] = df.apply(
    lambda x: return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["debt_to_equity"] = df.apply(
    lambda x: debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda x: interest_coverage(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda x: asset_turnover(
        x["sales"],
        x["fixed_assets"] +
        x["cwip"] +
        x["investments"] +
        x["other_asset"]
    ),
    axis=1
)

# Save output
df.to_csv(
    "output/financial_ratios_generated.csv",
    index=False
)

print("Financial ratios generated successfully.")
print("Rows:", len(df))