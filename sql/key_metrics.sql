-- Superstore Sales Analysis: headline numbers in SQL
-- Runs on SQLite 3.25+ (window functions). Load the data with:
--     python scripts/run_sql.py
-- which reads data/raw/superstore.csv into a table named `superstore`
-- and runs every query below in order.
--
-- Skills shown: CTEs, date parsing, GROUP BY aggregation, CASE pivots,
-- window functions (LAG, SUM OVER, NTILE, ROW_NUMBER).

-- 0. Clean view: the source dates are DD/MM/YYYY, so rebuild them as ISO dates.
DROP VIEW IF EXISTS sales;
CREATE VIEW sales AS
SELECT
    "Order ID"      AS order_id,
    "Customer ID"   AS customer_id,
    Segment         AS segment,
    Region          AS region,
    State           AS state,
    Category        AS category,
    "Sub-Category"  AS sub_category,
    "Ship Mode"     AS ship_mode,
    substr("Order Date", 7, 4) || '-' || substr("Order Date", 4, 2) || '-' || substr("Order Date", 1, 2) AS order_date,
    substr("Ship Date", 7, 4)  || '-' || substr("Ship Date", 4, 2)  || '-' || substr("Ship Date", 1, 2)  AS ship_date,
    CAST(Sales AS REAL) AS sales
FROM superstore;

-- 1. Headline KPIs
SELECT
    COUNT(*)                                   AS order_lines,
    COUNT(DISTINCT order_id)                   AS orders,
    COUNT(DISTINCT customer_id)                AS customers,
    ROUND(SUM(sales), 0)                       AS total_sales,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM sales;

-- 2. Yearly sales and year-over-year growth
WITH yearly AS (
    SELECT substr(order_date, 1, 4) AS year, SUM(sales) AS sales
    FROM sales
    GROUP BY year
)
SELECT
    year,
    ROUND(sales, 0) AS sales,
    ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY year)) / LAG(sales) OVER (ORDER BY year), 1) AS yoy_growth_pct
FROM yearly
ORDER BY year;

-- 3. Seasonality: share of all sales by calendar month
WITH monthly AS (
    SELECT CAST(substr(order_date, 6, 2) AS INTEGER) AS month, SUM(sales) AS sales
    FROM sales
    GROUP BY month
)
SELECT
    month,
    ROUND(sales, 0) AS sales,
    ROUND(100.0 * sales / SUM(sales) OVER (), 1) AS pct_of_total
FROM monthly
ORDER BY month;

-- 4. The back half of the year: Sep to Dec, Q4, and Jan + Feb
SELECT
    ROUND(100.0 * SUM(CASE WHEN CAST(substr(order_date, 6, 2) AS INTEGER) BETWEEN 9 AND 12 THEN sales END) / SUM(sales), 1) AS sep_to_dec_pct,
    ROUND(100.0 * SUM(CASE WHEN CAST(substr(order_date, 6, 2) AS INTEGER) BETWEEN 10 AND 12 THEN sales END) / SUM(sales), 1) AS q4_pct,
    ROUND(100.0 * SUM(CASE WHEN CAST(substr(order_date, 6, 2) AS INTEGER) IN (1, 2) THEN sales END) / SUM(sales), 1) AS jan_feb_pct
FROM sales;

-- 5. Segment growth, 2015 vs 2018 (CASE pivot)
SELECT
    segment,
    ROUND(SUM(sales), 0) AS total_sales,
    ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM sales), 1) AS pct_of_total,
    ROUND(SUM(CASE WHEN order_date LIKE '2015%' THEN sales END), 0) AS sales_2015,
    ROUND(SUM(CASE WHEN order_date LIKE '2018%' THEN sales END), 0) AS sales_2018,
    ROUND(100.0 * (SUM(CASE WHEN order_date LIKE '2018%' THEN sales END)
                 - SUM(CASE WHEN order_date LIKE '2015%' THEN sales END))
                 / SUM(CASE WHEN order_date LIKE '2015%' THEN sales END), 0) AS growth_2015_to_2018_pct
FROM sales
GROUP BY segment
ORDER BY total_sales DESC;

-- 6. Average order value by segment (sum lines into orders first)
WITH order_totals AS (
    SELECT segment, order_id, SUM(sales) AS order_total
    FROM sales
    GROUP BY segment, order_id
)
SELECT
    segment,
    COUNT(*)                   AS orders,
    ROUND(AVG(order_total), 2) AS avg_order_value
FROM order_totals
GROUP BY segment
ORDER BY avg_order_value;

-- 7. Region share and growth
SELECT
    region,
    ROUND(SUM(sales), 0) AS total_sales,
    ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM sales), 1) AS pct_of_total,
    ROUND(100.0 * (SUM(CASE WHEN order_date LIKE '2018%' THEN sales END)
                 - SUM(CASE WHEN order_date LIKE '2015%' THEN sales END))
                 / SUM(CASE WHEN order_date LIKE '2015%' THEN sales END), 0) AS growth_2015_to_2018_pct
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- 8. Top 5 states and sub-categories by share of sales
WITH state_rank AS (
    SELECT 'state' AS kind, state AS name, SUM(sales) AS sales,
           ROW_NUMBER() OVER (ORDER BY SUM(sales) DESC) AS rnk
    FROM sales GROUP BY state
), sub_rank AS (
    SELECT 'sub_category' AS kind, sub_category AS name, SUM(sales) AS sales,
           ROW_NUMBER() OVER (ORDER BY SUM(sales) DESC) AS rnk
    FROM sales GROUP BY sub_category
)
SELECT kind, rnk, name,
       ROUND(100.0 * sales / (SELECT SUM(sales) FROM sales), 1) AS pct_of_total
FROM (SELECT * FROM state_rank UNION ALL SELECT * FROM sub_rank)
WHERE rnk <= 5
ORDER BY kind, rnk;

-- 9. Shipping by mode, counted per order (every line in an order ships together)
WITH orders AS (
    SELECT DISTINCT order_id, ship_mode,
           julianday(ship_date) - julianday(order_date) AS days_to_ship
    FROM sales
)
SELECT
    ship_mode,
    COUNT(*) AS orders,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders,
    ROUND(AVG(days_to_ship), 2) AS avg_days_to_ship,
    MIN(days_to_ship) AS min_days,
    MAX(days_to_ship) AS max_days
FROM orders
GROUP BY ship_mode
ORDER BY avg_days_to_ship;

-- 10. Customer loyalty: repeat buyers and how concentrated sales are
WITH customers AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS orders, SUM(sales) AS sales
    FROM sales
    GROUP BY customer_id
), ranked AS (
    SELECT *, NTILE(5) OVER (ORDER BY sales DESC) AS quintile
    FROM customers
)
SELECT
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 0) AS repeat_buyer_pct,
    ROUND(100.0 * SUM(CASE WHEN quintile = 1 THEN sales END) / SUM(sales), 0) AS top_20pct_customer_share
FROM ranked;
