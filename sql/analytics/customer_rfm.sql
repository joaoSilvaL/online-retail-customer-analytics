
WITH valid_orders AS (
    SELECT
        customer_id,
        invoice,
        date(MIN(invoicedate)) AS order_date,
        SUM(quantity * price) AS order_value

    FROM transactions

    WHERE customer_id IS NOT NULL
        AND invoice NOT LIKE 'C%'
        AND quantity > 0
        AND price > 0
        AND date(invoicedate) <= date(:reference_date)

    GROUP BY customer_id, invoice
),

customer_rfm AS (
    SELECT
        customer_id,

        CAST(
            julianday(:reference_date)
            - julianday(MAX(order_date))
            AS INTEGER
        ) AS recency,

        COUNT(DISTINCT invoice) AS frequency,

        ROUND(SUM(order_value), 2) AS monetary,

        ROUND(AVG(order_value), 2) AS avg_order_value,

        MIN(order_date) AS first_purchase,

        MAX(order_date) AS last_purchase

    FROM valid_orders

    GROUP BY customer_id
)

SELECT *
FROM customer_rfm
ORDER BY customer_id;
