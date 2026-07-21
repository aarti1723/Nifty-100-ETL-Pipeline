import sqlite3
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ---------------- Database ----------------

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.free_cash_flow_cr,
    a.compounded_sales_growth,
    s.broad_sector

FROM financial_ratios fr

LEFT JOIN analysis a
ON fr.company_id = a.company_id

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.id IN
(
    SELECT MAX(id)
    FROM financial_ratios
    GROUP BY company_id
)
"""

df = pd.read_sql(query, conn)

conn.close()

print(df.head())
print("Rows :", len(df))

# ---------------- Numeric Conversion ----------------

numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "compounded_sales_growth"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------- Remove Invalid Data ----------------

df = df[
    (df["return_on_equity_pct"] <= 100) &
    (df["operating_profit_margin_pct"].between(-100, 100))
]

print("\nRows after cleaning:", len(df))

# ---------------- Feature Selection ----------------

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "compounded_sales_growth"
]

X = df[features]

print("\nMissing Values:")
print(X.isna().sum())

# ---------------- Missing Value Imputation ----------------

imputer = SimpleImputer(strategy="median")

X_imputed = imputer.fit_transform(X)

# ---------------- Standard Scaling ----------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X_imputed)

print("\nScaling Completed")
print(X_scaled[:5])

# ---------------- Elbow Method ----------------

wcss = []

for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(
    range(2,11),
    wcss,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Clusters")
plt.ylabel("WCSS")
plt.grid(True)

plt.savefig("reports/elbow_plot.png")

plt.close()

print("\nElbow Plot Saved")

# ---------------- Final Clustering ----------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

df["cluster"] = kmeans.fit_predict(X_scaled)

df.to_csv(
    "output/cluster_labels.csv",
    index=False
)

print("\nClustering Completed")
print(df[["company_id", "cluster"]].head())

# ---------------- Duplicate Check ----------------

duplicates = df["company_id"].value_counts()
duplicates = duplicates[duplicates > 1]

if duplicates.empty:
    print("\nNo Duplicate Companies Found ✅")
else:
    print("\nDuplicate Companies:")
    print(duplicates)

# ---------------- Cluster Summary ----------------

summary = df.groupby("cluster").agg(
    companies=("company_id", "count"),
    avg_roe=("return_on_equity_pct", "mean"),
    avg_debt=("debt_to_equity", "mean"),
    avg_opm=("operating_profit_margin_pct", "mean"),
    avg_sales_growth=("compounded_sales_growth", "mean")
).round(2)

print("\nCluster Summary")
print(summary)

summary.to_csv(
    "output/cluster_summary.csv"
)

print("\ncluster_summary.csv Saved Successfully ✅")