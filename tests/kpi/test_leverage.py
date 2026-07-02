from src.analytics.ratios import *

def test_debt_to_equity():
    assert debt_to_equity(500, 1000, 500) == 500 / 1500

def test_debt_free():
    assert debt_to_equity(0, 1000, 500) == 0

def test_negative_equity():
    assert debt_to_equity(500, -1000, 500) is None

def test_interest_coverage():
    assert interest_coverage(500, 100, 100) == 6

def test_interest_zero():
    assert interest_coverage(500, 100, 0) is None

def test_icr_label():
    assert icr_label(0) == "Debt Free"

def test_net_debt():
    assert net_debt(1000, 300) == 700

def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2