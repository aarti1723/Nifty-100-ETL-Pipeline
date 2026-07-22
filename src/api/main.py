from fastapi import FastAPI
from src.api.database import get_connection

app = FastAPI(
    title="Nifty100 API",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "Nifty100 API Running Successfully"}


@app.get("/companies")
def companies():
    conn = get_connection()
    data = conn.execute(
        "SELECT * FROM companies"
    ).fetchall()
    conn.close()

    return [dict(x) for x in data]


@app.get("/company/{company_id}")
def company(company_id: str):

    conn = get_connection()

    data = conn.execute(
        """
        SELECT *
        FROM companies
        WHERE id=?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if data:
        return dict(data)

    return {"error": "Company not found"}
@app.get("/financial-ratios/{company_id}")
def financial_ratios(company_id: str):

    conn = get_connection()

    data = conn.execute(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if data:
        return dict(data)

    return {"error": "Financial Ratios not found"}

@app.get("/analysis/{company_id}")
def analysis(company_id: str):

    conn = get_connection()

    data = conn.execute(
        """
        SELECT *
        FROM analysis
        WHERE company_id=?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if data:
        return dict(data)

    return {"error": "Analysis not found"}

@app.get("/sector/{company_id}")
def sector(company_id: str):

    conn = get_connection()

    data = conn.execute(
        """
        SELECT *
        FROM sectors
        WHERE company_id=?
        """,
        (company_id,)
    ).fetchone()

    conn.close()

    if data:
        return dict(data)

    return {"error": "Sector not found"}

@app.get("/market-cap")
def market_cap():

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM market_cap
    """).fetchall()

    conn.close()

    return [dict(i) for i in data]

@app.get("/peer-groups")
def peer_groups():

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM peer_groups
    """).fetchall()

    conn.close()

    return [dict(i) for i in data]

@app.get("/peer-percentiles")
def peer_percentiles():

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM peer_percentiles
    """).fetchall()

    conn.close()

    return [dict(i) for i in data]


@app.get("/cashflow/{company_id}")
def cashflow(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM cashflow
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]
@app.get("/balancesheet/{company_id}")
def balancesheet(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM balancesheet
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]

@app.get("/profit-loss/{company_id}")
def profit_loss(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM profitandloss
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]


@app.get("/documents/{company_id}")
def documents(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM documents
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]

@app.get("/pros-cons/{company_id}")
def pros_cons(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM prosandcons
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]


@app.get("/stock-price/{company_id}")
def stock_price(company_id: str):

    conn = get_connection()

    data = conn.execute("""
    SELECT *
    FROM stock_prices
    WHERE company_id=?
    """,(company_id,)).fetchall()

    conn.close()

    return [dict(i) for i in data]

@app.get("/health")
def health():

    return {
        "status":"Running",
        "database":"Connected",
        "api":"Healthy"
    }

