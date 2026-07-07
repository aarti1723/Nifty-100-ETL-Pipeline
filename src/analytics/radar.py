import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT
company_id,
return_on_equity_pct,
operating_profit_margin_pct,
net_profit_margin_pct,
debt_to_equity,
interest_coverage,
asset_turnover
FROM financial_ratios
""", conn)

peer = pd.read_sql("SELECT * FROM peer_groups", conn)

conn.close()

data = df.merge(peer,on="company_id",how="inner")

os.makedirs("reports/radar_charts",exist_ok=True)

metrics=[
"return_on_equity_pct",
"operating_profit_margin_pct",
"net_profit_margin_pct",
"debt_to_equity",
"interest_coverage",
"asset_turnover"
]

angles=np.linspace(
0,
2*np.pi,
len(metrics),
endpoint=False
).tolist()

angles+=angles[:1]

count=0

for company in data.company_id.unique():

    temp=data[data.company_id==company]

    latest=temp.iloc[-1]

    values=[]

    for m in metrics:

        values.append(float(latest[m]))

    values+=values[:1]

    plt.figure(figsize=(6,6))

    ax=plt.subplot(111,polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(metrics,fontsize=8)

    plt.title(company)

    plt.savefig(
        f"reports/radar_charts/{company}_radar.png",
        dpi=150
    )

    plt.close()

    count+=1

print("Radar Charts:",count)