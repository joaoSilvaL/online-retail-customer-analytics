SELECT
    date(invoicedate) AS reference_date,
    COUNT(DISTINCT customer_id) AS dau
FROM transactions
WHERE customer_id IS NOT NULL
    AND invoice NOT LIKE 'C%'
    AND quantity > 0
    AND price > 0
GROUP BY date(invoicedate)
ORDER BY reference_date;
