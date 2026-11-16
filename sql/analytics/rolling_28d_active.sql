
WITH daily_customers AS (
    SELECT DISTINCT
        date(invoicedate) AS reference_date,
        customer_id
    FROM transactions
    WHERE customer_id IS NOT NULL
        AND invoice NOT LIKE 'C%'
        AND quantity > 0
        AND price > 0
),

reference_dates AS (
    SELECT DISTINCT reference_date
    FROM daily_customers
)

SELECT
    r.reference_date,
    COUNT(DISTINCT d.customer_id) AS active_customers_28d
FROM reference_dates r
LEFT JOIN daily_customers d
    ON d.reference_date <= r.reference_date
    AND julianday(r.reference_date)
        - julianday(d.reference_date) < 28
GROUP BY r.reference_date
ORDER BY r.reference_date;
