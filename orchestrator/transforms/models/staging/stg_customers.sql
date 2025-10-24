select
    customer_id,
    customer_name,
    email,
    signup_date,
    tier,
    valid_from,
    valid_to,
    is_current
from {{ source('metadata', 'raw_customers') }}
