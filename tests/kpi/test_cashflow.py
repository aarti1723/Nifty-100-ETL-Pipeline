from src.analytics.cashflow_kpis import *

def test_fcf():
    assert free_cash_flow(100, -20) == 80

def test_quality_high():
    assert cfo_quality_score(120, 100) == "High Quality"

def test_quality_moderate():
    assert cfo_quality_score(70, 100) == "Moderate"

def test_quality_risk():
    assert cfo_quality_score(30, 100) == "Accrual Risk"

def test_quality_none():
    assert cfo_quality_score(100, 0) is None

def test_capex():
    assert capex_intensity(-100, 1000) == 10

def test_capex_none():
    assert capex_intensity(-100, 0) is None

def test_fcf_conversion():
    assert fcf_conversion(100, 200) == 50