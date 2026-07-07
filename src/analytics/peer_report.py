import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

peer = pd.read_sql(
    "SELECT * FROM peer_percentiles",
    conn
)

groups = pd.read_sql(
    "SELECT DISTINCT peer_group_name FROM peer_groups",
    conn
)

writer = pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
)

for group in groups["peer_group_name"]:

    temp = peer[
        peer["peer_group_name"] == group
    ]

    temp.to_excel(
        writer,
        sheet_name=group[:31],
        index=False
    )

writer.close()

conn.close()

print("peer_comparison.xlsx generated successfully.")