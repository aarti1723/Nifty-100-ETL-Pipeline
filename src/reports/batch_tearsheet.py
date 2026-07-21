import sqlite3
import pandas as pd
import subprocess
import os

os.makedirs("reports/tearsheets", exist_ok=True)
os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("""
SELECT id
FROM companies
ORDER BY id
""", conn)


conn.close()

generated = []
skipped = []

print(f"Generating {len(companies)} PDFs...\n")

for cid in companies["id"]:

    try:

        subprocess.run(
            [
                "python",
                "src/reports/tearsheet.py",
                cid
            ],
            check=True
        )

        generated.append(cid)

    except Exception as e:
        print(f"\n❌ Failed : {cid}")
        print(e)
        skipped.append(cid)

pd.DataFrame({
    "company_id": skipped
}).to_csv(
    "output/skipped_tearsheets.csv",
    index=False
)

print("\n=========================")
print("Generated :", len(generated))
print("Skipped   :", len(skipped))
print("=========================")