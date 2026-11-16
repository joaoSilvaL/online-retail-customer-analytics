SELECT
    strftime('%Y-%m', invoicedate) AS reference_month,
    COUNT(DISTINCT customer_id) AS mau
FROM transactions
WHERE customer_id IS NOT NULL
    AND invoice NOT LIKE 'C%'
    AND quantity > 0
    AND price > 0
GROUP BY strftime('%Y-%m', invoicedate)
ORDER BY reference_month;
