-- 1
SELECT COUNT(*) FROM companies;

-- 2
SELECT company_name
FROM companies
LIMIT 10;

-- 3
SELECT company_id, MAX(sales)
FROM profitandloss
GROUP BY company_id
ORDER BY MAX(sales) DESC
LIMIT 10;

-- 4
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 5
SELECT company_id, return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;

-- 6
SELECT company_id, close
FROM stock_prices
ORDER BY close DESC
LIMIT 10;

-- 7
SELECT company_id, COUNT(*)
FROM stock_prices
GROUP BY company_id
ORDER BY COUNT(*) DESC;

-- 8
SELECT company_id, debt_to_equity
FROM financial_ratios
ORDER BY debt_to_equity DESC
LIMIT 10;

-- 9
SELECT company_id, free_cash_flow_cr
FROM financial_ratios
ORDER BY free_cash_flow_cr DESC
LIMIT 10;

-- 10
SELECT sector_name, COUNT(*)
FROM sectors
GROUP BY sector_name;