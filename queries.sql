-- 1. Revenue by region
SELECT c.region,
       COUNT(DISTINCT o.id)              AS orders,
       ROUND(SUM(oi.quantity * p.price), 2) AS revenue
FROM orders o
JOIN customers c   ON c.id = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products p    ON p.id = oi.product_id
GROUP BY c.region
ORDER BY revenue DESC;

-- 2. Monthly revenue with month-over-month change
WITH monthly AS (
  SELECT strftime('%Y-%m', o.order_date) AS month,
         SUM(oi.quantity * p.price)      AS revenue
  FROM orders o
  JOIN order_items oi ON oi.order_id = o.id
  JOIN products p     ON p.id = oi.product_id
  GROUP BY month
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 1) AS pct_change
FROM monthly
ORDER BY month;

-- 3. Top 5 products by revenue
SELECT p.name, p.category,
       SUM(oi.quantity)                     AS units_sold,
       ROUND(SUM(oi.quantity * p.price), 2) AS revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id
ORDER BY revenue DESC
LIMIT 5;
