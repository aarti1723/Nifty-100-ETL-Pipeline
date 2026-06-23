import pandas as pd

files = [
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx"
]

for f in files:
    print("\n" + "="*50)
    print(f)

    df = pd.read_excel("data/" + f, header=None)

    print(df.head(3))
    print("Columns:", len(df.columns))