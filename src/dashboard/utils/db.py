import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_data(ttl=600)
def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_ratios(ticker, year=None):
    conn = get_connection()

    if year:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        AND year=?
        """
        df = pd.read_sql(
            query,
            conn,
            params=(ticker, year)
        )
    else:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        """
        df = pd.read_sql(
            query,
            conn,
            params=(ticker,)
        )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM profitandloss WHERE company_id=?",
        conn,
        params=(ticker,)
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM balancesheet WHERE company_id=?",
        conn,
        params=(ticker,)
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM cashflow WHERE company_id=?",
        conn,
        params=(ticker,)
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name=?
        """,
        conn,
        params=(group_name,)
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation(ticker):
    conn = get_connection()

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM valuation_summary
            WHERE company_id=?
            """,
            conn,
            params=(ticker,)
        )
    except:
        df = pd.DataFrame()

    conn.close()
    return df