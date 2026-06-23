from src.etl.validator import dq06_positive_sales
import pandas as pd

def test_positive_sales():
    df = pd.DataFrame({
        "sales":[100,200,-10]
    })

    failures = dq06_positive_sales(df)

    assert len(failures) == 1