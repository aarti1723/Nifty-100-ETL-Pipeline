import pandas as pd

files = [
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "profitandloss.xlsx",
    "financial_ratios.xlsx",
    "stock_prices.xlsx"
]

for f in files:
    print("\n" + "="*50)
    print(f)

    df = pd.read_excel("data/" + f, header=1)

    print(df.head(2))
    print(df.columns.tolist())