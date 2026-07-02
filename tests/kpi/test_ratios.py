from src.analytics.ratios import *

def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None

def test_operating_profit_margin():
    assert operating_profit_margin(200, 1000) == 20.0

def test_operating_profit_margin_zero_sales():
    assert operating_profit_margin(200, 0) is None

def test_return_on_equity():
    assert round(return_on_equity(500, 1000, 500), 2) == 33.33

def test_return_on_equity_negative():
    assert return_on_equity(500, -1000, 500) is None

def test_return_on_capital_employed():
    assert round(return_on_capital_employed(400, 1000, 500, 500), 2) == 20.00

def test_return_on_assets():
    assert return_on_assets(100, 1000) == 10.0