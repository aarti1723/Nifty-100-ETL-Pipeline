import pandas as pd


def quality_compounder(df):
    return df[
        (df["return_on_equity_pct"] > 18)
        &
        (df["debt_to_equity"] < 0.5)
        &
        (df["operating_profit_margin_pct"] > 20)
        &
        (df["asset_turnover"] > 1)
    ]


def value_pick(df):
    return df[
        (df["debt_to_equity"] < 0.5)
        &
        (df["return_on_equity_pct"] > 15)
        &
        (df["operating_profit_margin_pct"] > 15)
    ]


def growth_accelerator(df):
    return df[
        (df["return_on_equity_pct"] > 22)
        &
        (df["asset_turnover"] > 1.2)
        &
        (df["operating_profit_margin_pct"] > 18)
    ]


def dividend_champion(df):

    if "dividend_payout" not in df.columns:
        return pd.DataFrame(columns=df.columns)

    return df[
        (df["dividend_payout"] >= 30)
        &
        (df["dividend_payout"] <= 70)
        &
        (df["return_on_equity_pct"] > 15)
    ]


def debt_free_bluechip(df):
    return df[
        (df["debt_to_equity"] <= 0.10)
        &
        (df["return_on_equity_pct"] > 15)
        &
        (df["operating_profit_margin_pct"] > 15)
    ]


def turnaround_watch(df):
    return df[
        (df["operating_profit_margin_pct"] > 15)
        &
        (df["return_on_equity_pct"] > 15)
        &
        (df["asset_turnover"] > 0.8)
    ]