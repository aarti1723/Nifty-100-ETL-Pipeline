from src.etl.normaliser import normalize_year, normalize_ticker
def test_year_01():
    assert normalize_year("Mar 2024") == "Mar 2024"

def test_year_02():
    assert normalize_year(" Mar 2024 ") == "Mar 2024"

def test_year_03():
    assert normalize_year(None) is None

def test_ticker_01():
    assert normalize_ticker("tcs") == "TCS"

def test_ticker_02():
    assert normalize_ticker(" tcs ") == "TCS"

def test_ticker_03():
    assert normalize_ticker(None) is None
def test_year_04():
    assert normalize_year("2024") == "2024"

def test_year_05():
    assert normalize_year(" 2024 ") == "2024"

def test_year_06():
    assert normalize_year("") == ""

def test_year_07():
    assert normalize_year("FY2024") == "FY2024"

def test_year_08():
    assert normalize_year("Mar 2023") == "Mar 2023"

def test_year_09():
    assert normalize_year("Mar 2022") == "Mar 2022"

def test_year_10():
    assert normalize_year("Mar 2021") == "Mar 2021"

def test_year_11():
    assert normalize_year(2024) == "2024"

def test_year_12():
    assert normalize_year("Q1 2024") == "Q1 2024"

def test_year_13():
    assert normalize_year("Q2 2024") == "Q2 2024"

def test_year_14():
    assert normalize_year("Q3 2024") == "Q3 2024"

def test_year_15():
    assert normalize_year("Q4 2024") == "Q4 2024"

def test_year_16():
    assert normalize_year("FY 2023") == "FY 2023"

def test_year_17():
    assert normalize_year("FY 2022") == "FY 2022"

def test_year_18():
    assert normalize_year("2020-21") == "2020-21"

def test_year_19():
    assert normalize_year("2019-20") == "2019-20"

def test_year_20():
    assert normalize_year("2018-19") == "2018-19"


def test_ticker_04():
    assert normalize_ticker("infy") == "INFY"

def test_ticker_05():
    assert normalize_ticker("reliance") == "RELIANCE"

def test_ticker_06():
    assert normalize_ticker(" hdfcbank ") == "HDFCBANK"

def test_ticker_07():
    assert normalize_ticker("sbin") == "SBIN"

def test_ticker_08():
    assert normalize_ticker("itc") == "ITC"

def test_ticker_09():
    assert normalize_ticker("lt") == "LT"

def test_ticker_10():
    assert normalize_ticker("asianpaint") == "ASIANPAINT"

def test_ticker_11():
    assert normalize_ticker("wipro") == "WIPRO"

def test_ticker_12():
    assert normalize_ticker("titan") == "TITAN"

def test_ticker_13():
    assert normalize_ticker("sunpharma") == "SUNPHARMA"

def test_ticker_14():
    assert normalize_ticker(" techm ") == "TECHM"

def test_ticker_15():
    assert normalize_ticker("nestleind") == "NESTLEIND"

def test_ticker_16():
    assert normalize_ticker("ultracemco") == "ULTRACEMCO"

def test_ticker_17():
    assert normalize_ticker("vedl") == "VEDL"

def test_ticker_18():
    assert normalize_ticker("") == ""