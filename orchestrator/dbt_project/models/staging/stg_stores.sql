select
    store_id,
    store_name,
    location,
    store_type,
    opened_date,
    valid_from,
    valid_to,
    is_current
from {{ source('lake', 'raw_stores') }}
