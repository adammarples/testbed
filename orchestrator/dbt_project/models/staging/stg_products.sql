select
    product_id,
    product_name,
    category,
    base_price
from {{ source('lake', 'raw_products') }}
