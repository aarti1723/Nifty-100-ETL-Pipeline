from src.analytics.cagr import *

def test_normal_cagr():
    assert round(calculate_cagr(100, 200, 5), 2) == 14.87

def test_zero_base():
    assert calculate_cagr(0, 100, 5) is None

def test_negative_to_positive():
    assert calculate_cagr(-100, 100, 5) is None

def test_positive_to_negative():
    assert calculate_cagr(100, -100, 5) is None

def test_negative_to_negative():
    assert calculate_cagr(-100, -200, 5) is None

def test_zero_year():
    assert calculate_cagr(100, 200, 0) is None

def test_revenue_cagr():
    assert round(revenue_cagr(100, 200, 5), 2) == 14.87

def test_pat_cagr():
    assert round(pat_cagr(100, 200, 5), 2) == 14.87

def test_eps_cagr():
    assert round(eps_cagr(100, 200, 5), 2) == 14.87

def test_same_value():
    assert calculate_cagr(100, 100, 5) == 0