import pandas as pd


def dq01_primary_key(df, column_name):
    duplicates = df[df[column_name].duplicated()]
    return duplicates


def dq02_company_year(df):
    duplicates = df[df.duplicated(
        subset=["company_id", "year"]
    )]
    return duplicates


def dq03_foreign_key(child_df, parent_df):
    valid_ids = set(parent_df["id"])

    failures = child_df[
        ~child_df["company_id"].isin(valid_ids)
    ]

    return failures


def dq06_positive_sales(df):
    failures = df[df["sales"] <= 0]
    return failures


if __name__ == "__main__":

    companies = pd.read_excel(
        "data/companies.xlsx",
        header=1
    )

    pnl = pd.read_excel(
        "data/profitandloss.xlsx",
        header=1
    )

    pk_failures = dq01_primary_key(
        pnl,
        "id"
    )

    company_year_failures = dq02_company_year(
        pnl
    )

    fk_failures = dq03_foreign_key(
        pnl,
        companies
    )

    sales_failures = dq06_positive_sales(
        pnl
    )

    print("PK failures:", len(pk_failures))

    print(
        "Company-Year failures:",
        len(company_year_failures)
    )

    print(
        "FK failures:",
        len(fk_failures)
    )

    print(
        "Sales failures:",
        len(sales_failures)
    )







#print("\nFK Failure Sample:")
#print(fk_failures[["company_id"]].head(10))

#print("\nSales Failure Sample:")
#print(sales_failures[["company_id", "year", "sales"]])





def dq04_balance_sheet(bs_df):

    lhs = (
        bs_df["equity_capital"]
        + bs_df["reserves"]
        + bs_df["borrowings"]
        + bs_df["other_liabilities"]
    )

    rhs = (
        bs_df["fixed_assets"]
        + bs_df["cwip"]
        + bs_df["investments"]
        + bs_df["other_asset"]
    )

    diff_pct = abs(lhs - rhs) / rhs * 100

    failures = bs_df[diff_pct > 1]

    return failures


#if __name__ == "__main__":


#all_failures = []

#if len(fk_failures) > 0:

    #temp = fk_failures.copy()

    #temp["rule"] = "DQ03_FK"

    #all_failures.append(temp)


if len(sales_failures) > 0:

    temp = sales_failures.copy()

    temp["rule"] = "DQ06_POSITIVE_SALES"

    all_failures.append(temp)


if len(company_year_failures) > 0:

    temp = company_year_failures.copy()

    temp["rule"] = "DQ02_COMPANY_YEAR"

    all_failures.append(temp)



if all_failures:

    failures_df = pd.concat(
        all_failures,
        ignore_index=True
    )

    failures_df.to_csv(
        "output/validation_failures.csv",
        index=False
    )

    print("\nvalidation_failures.csv created")




def dq04_balance_sheet(bs_df):

    liabilities = (
        bs_df["equity_capital"]
        + bs_df["reserves"]
        + bs_df["borrowings"]
        + bs_df["other_liabilities"]
    )

    assets = (
        bs_df["fixed_assets"]
        + bs_df["cwip"]
        + bs_df["investments"]
        + bs_df["other_asset"]
    )

    diff_pct = abs(liabilities - assets) / assets * 100

    failures = bs_df[diff_pct > 1]

    return failures





bs = pd.read_excel(
    "data/balancesheet.xlsx",
    header=1
)

bs_failures = dq04_balance_sheet(bs)

print(
    "Balance Sheet failures:",
    len(bs_failures)
)


pl = pd.read_excel(
    "data/profitandloss.xlsx",
    header=1
)

def dq05_opm_check(pl_df):

    calculated_opm = (
        pl_df["operating_profit"] /
        pl_df["sales"]
    ) * 100

    diff = abs(
        calculated_opm -
        pl_df["opm_percentage"]
    )

    failures = pl_df[
        (pl_df["sales"] > 0) &
        (diff > 1)
    ]

    return failures

opm_failures = dq05_opm_check(pl)

print(
    "OPM failures:",
    len(opm_failures)
)



def dq07_roe_range(df):
    return df[(df["return_on_equity_pct"] < -100) |
              (df["return_on_equity_pct"] > 100)]

def dq08_de_ratio(df):
    return df[df["debt_to_equity"] < 0]

def dq09_interest_coverage(df):
    return df[df["interest_coverage"] < 0]

def dq10_eps_check(df):
    return df[df["earnings_per_share"].isna()]

def dq11_book_value_check(df):
    return df[df["book_value_per_share"] <= 0]

def dq12_dividend_ratio(df):
    return df[
        (df["dividend_payout_ratio_pct"] < 0) |
        (df["dividend_payout_ratio_pct"] > 100)
    ]

def dq13_asset_turnover(df):
    return df[df["asset_turnover"] < 0]

def dq14_net_profit_margin(df):
    return df[(df["net_profit_margin_pct"] < -100) |
              (df["net_profit_margin_pct"] > 100)]

def dq15_document_url(df):
    return df[df["Annual_Report"].isna()]

def dq16_growth_fields(df):
    return df[
        df["compounded_sales_growth"].isna() |
        df["compounded_profit_growth"].isna()
    ]

ratios = pd.read_excel(
    "data/financial_ratios.xlsx",
    header=0
)

analysis_df = pd.read_excel(
    "data/analysis.xlsx",
    header=1
)

documents_df = pd.read_excel(
    "data/documents.xlsx",
    header=1
)

print("DQ07:", len(dq07_roe_range(ratios)))
print("DQ08:", len(dq08_de_ratio(ratios)))
print("DQ09:", len(dq09_interest_coverage(ratios)))
print("DQ10:", len(dq10_eps_check(ratios)))
print("DQ11:", len(dq11_book_value_check(ratios)))
print("DQ12:", len(dq12_dividend_ratio(ratios)))
print("DQ13:", len(dq13_asset_turnover(ratios)))
print("DQ14:", len(dq14_net_profit_margin(ratios)))
print("DQ15:", len(dq15_document_url(documents_df)))
print("DQ16:", len(dq16_growth_fields(analysis_df)))