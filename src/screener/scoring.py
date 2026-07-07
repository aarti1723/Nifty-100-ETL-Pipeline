import pandas as pd


def normalize(series):
    s = series.fillna(0)

    minimum = s.min()
    maximum = s.max()

    if maximum == minimum:
        return pd.Series([50] * len(s), index=s.index)

    return ((s - minimum) / (maximum - minimum)) * 100


def sector_composite(df):

    df = df.copy()

    df["roe_score"] = normalize(df["return_on_equity_pct"])
    df["opm_score"] = normalize(df["operating_profit_margin_pct"])
    df["asset_score"] = normalize(df["asset_turnover"])

    debt_score = 100 - normalize(df["debt_to_equity"])

    df["composite_quality_score"] = (
        df["roe_score"] * 0.40
        + df["opm_score"] * 0.25
        + df["asset_score"] * 0.15
        + debt_score * 0.20
    )

    return df.sort_values(
        "composite_quality_score",
        ascending=False
    )