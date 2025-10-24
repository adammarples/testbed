with sales as (
    select * from {{ ref('stg_sales') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
    where is_current = true
),

customer_sales as (
    select
        s.customer_id,
        count(distinct s.transaction_id) as total_purchases,
        sum(s.amount) as lifetime_value,
        min(s.sale_date) as first_purchase_date,
        max(s.sale_date) as last_purchase_date,
        avg(s.amount) as avg_purchase_amount
    from sales s
    group by s.customer_id
)

select
    c.customer_id,
    c.customer_name,
    c.email,
    c.tier,
    c.signup_date,
    coalesce(cs.total_purchases, 0) as total_purchases,
    coalesce(cs.lifetime_value, 0) as lifetime_value,
    cs.first_purchase_date,
    cs.last_purchase_date,
    coalesce(cs.avg_purchase_amount, 0) as avg_purchase_amount
from customers c
left join customer_sales cs on c.customer_id = cs.customer_id
