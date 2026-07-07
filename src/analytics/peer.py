import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peers = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

df = ratios.merge(
    peers,
    on="company_id",
    how="left"
)

metrics = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover"
]

records = []

for group in df["peer_group_name"].dropna().unique():

    temp = df[df["peer_group_name"] == group].copy()

    for metric in metrics:

        if metric not in temp.columns:
            continue

        if metric == "debt_to_equity":
            temp["percentile"] = (
                1 -
                temp[metric].rank(pct=True)
            )

        else:
            temp["percentile"] = (
                temp[metric].rank(pct=True)
            )

        for _, row in temp.iterrows():

            records.append({

                "company_id":
                    row["company_id"],

                "peer_group_name":
                    group,

                "metric":
                    metric,

                "value":
                    row[metric],

                "percentile_rank":
                    round(
                        row["percentile"] * 100,
                        2
                    ),

                "year":
                    row["year"]

            })

peer = pd.DataFrame(records)

peer.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

peer.to_csv(
    "output/peer_percentiles.csv",
    index=False
)

print(peer.head())

print("\nRows:", len(peer))

conn.close()