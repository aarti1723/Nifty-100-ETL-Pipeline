import pandas as pd

files = [
"analysis.xlsx",
"documents.xlsx",
"prosandcons.xlsx"
]

for f in files:
    print("\n" + "="*50)
    print(f)
    
df = pd.read_excel("data/" + f, header=1)

print(df.head())
print(df.columns.tolist())