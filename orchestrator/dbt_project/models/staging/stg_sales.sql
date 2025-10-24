select
    transaction_id,
    customer_id,
    store_id,
    product_id,
    sale_date,
    quantity,
    unit_price,
    amount
from {{ source('metadata', 'raw_sales') }}
