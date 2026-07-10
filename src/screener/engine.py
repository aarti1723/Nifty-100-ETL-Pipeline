import yaml
import pandas as pd
import sqlite3

from src.screener.scoring import sector_composite
from src.screener.presets import (
    value_pick,
    growth_accelerator,
    dividend_champion,
    debt_free_bluechip,
    turnaround_watch,
)


def load_config():
    with open("config/screener_config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_data():
    conn = sqlite3.connect("db/nifty100.db")

    query = """
WITH latest AS (
    SELECT
        company_id,
        MAX(year) AS year
    FROM financial_ratios
    GROUP BY company_id
)

SELECT *
FROM financial_ratios fr
JOIN latest l
    ON fr.company_id = l.company_id
   AND fr.year = l.year
JOIN profitandloss pl
    ON fr.company_id = pl.company_id
   AND fr.year = pl.year
JOIN balancesheet bs
    ON fr.company_id = bs.company_id
   AND fr.year = bs.year
"""

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def quality_compounder(df, config):

    roe = config["filters"]["return_on_equity_pct"]["min"]
    de = config["filters"]["debt_to_equity"]["max"]
    opm = config["filters"]["operating_profit_margin_pct"]["min"]

    return df[
        (df["return_on_equity_pct"] > roe)
        &
        (df["debt_to_equity"] < de)
        &
        (df["operating_profit_margin_pct"] > opm)
    ]


def composite_score(df):

    df = df.copy()

    score = (
        df["return_on_equity_pct"].fillna(0) * 0.35
        + df["operating_profit_margin_pct"].fillna(0) * 0.25
        + df["asset_turnover"].fillna(0) * 0.20
        + (1 / (df["debt_to_equity"] + 1)).fillna(0) * 20
    )

    df["composite_quality_score"] = score

    return df.sort_values(
        "composite_quality_score",
        ascending=False
    )


if __name__ == "__main__":

    config = load_config()

    df = load_data()

    screeners = {
        "Quality Compounder": quality_compounder(df, config),
        "Value Pick": value_pick(df),
        "Growth Accelerator": growth_accelerator(df),
        "Dividend Champion": dividend_champion(df),
        "Debt Free Bluechip": debt_free_bluechip(df),
        "Turnaround Watch": turnaround_watch(df),
    }

    with pd.ExcelWriter("output/screener_output.xlsx") as writer:

        for name, screener_df in screeners.items():

            if len(screener_df) > 0:
                screener_df = sector_composite(screener_df)

            screener_df.to_excel(
                writer,
                sheet_name=name[:31],
                index=False
            )

            print(f"{name}: {len(screener_df)} companies")

    print("\nSprint 3 completed successfully.")