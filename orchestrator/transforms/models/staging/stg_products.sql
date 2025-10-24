select
    product_id,
    product_name,
    category,
    base_price
from {{ source('metadata', 'raw_products') }}
