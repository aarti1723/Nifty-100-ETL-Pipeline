import pandas as pd
import sqlite3

from src.screener.scoring import sector_composite
from src.screener.presets import (
    quality_compounder,
    value_pick,
    growth_accelerator,
    dividend_champion,
    debt_free_bluechip,
    turnaround_watch,
)


def load_data():
    conn = sqlite3.connect("db/nifty100.db")

    query = """
    SELECT *
    FROM financial_ratios fr
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


def quality_compounder(df):
    return df[
        (df["return_on_equity_pct"] > 15)
        &
        (df["debt_to_equity"] < 1)
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

    df = load_data()

    screeners = {
        "Quality Compounder": quality_compounder(df),
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

    print("\nSprint 3 Day 16 completed successfully.")