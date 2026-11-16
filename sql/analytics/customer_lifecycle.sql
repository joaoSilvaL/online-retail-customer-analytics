
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
        AND date(invoicedate) <= date('2011-12-10')

    GROUP BY customer_id, invoice
),

order_history AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC, invoice DESC
        ) AS rn

    FROM valid_orders
),

customer_summary AS (
    SELECT
        customer_id,

        MIN(order_date) AS first_purchase,
        MAX(order_date) AS last_purchase,

        COUNT(DISTINCT invoice) AS total_orders,

        MAX(
            CASE WHEN rn = 2 THEN order_date END
        ) AS previous_purchase

    FROM order_history
    GROUP BY customer_id
),

customer_metrics AS (
    SELECT
        c.*,

        CAST(
            julianday('2011-12-10')
            - julianday(c.first_purchase)
            AS INTEGER
        ) AS days_since_first_purchase,

        CAST(
            julianday('2011-12-10')
            - julianday(c.last_purchase)
            AS INTEGER
        ) AS days_since_last_purchase,

        CAST(
            julianday(c.last_purchase)
            - julianday(c.previous_purchase)
            AS INTEGER
        ) AS days_between_purchases,

        COUNT(
            CASE
                WHEN o.order_date > date('2011-12-10', '-28 days')
                THEN 1
            END
        ) AS orders_28d,

        ROUND(
            COALESCE(
                SUM(
                    CASE
                        WHEN o.order_date > date('2011-12-10', '-28 days')
                        THEN o.order_value
                        ELSE 0
                    END
                ),
                0
            ),
            2
        ) AS revenue_28d

    FROM customer_summary c

    LEFT JOIN valid_orders o
        ON c.customer_id = o.customer_id

    GROUP BY c.customer_id
),

customer_lifecycle AS (
    SELECT
        *,

        CASE
            WHEN days_since_first_purchase <= 7
                 AND total_orders = 1
                THEN '01-NOVO'

            WHEN days_since_last_purchase <= 28
                 AND days_between_purchases > 60
                THEN '02-REATIVADO'

            WHEN days_since_last_purchase <= 28
                THEN '03-ATIVO'

            WHEN days_since_last_purchase BETWEEN 29 AND 60
                THEN '04-EM_RISCO'

            WHEN days_since_last_purchase > 60
                THEN '05-INATIVO'

        END AS lifecycle_stage

    FROM customer_metrics
)

SELECT
    date('2011-12-10') AS'2011-12-10',
    *

FROM customer_lifecycle
ORDER BY customer_id;
