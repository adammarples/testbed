with sales as (
    select * from {{ ref('stg_sales') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

product_sales as (
    select
        s.product_id,
        count(distinct s.transaction_id) as times_sold,
        sum(s.quantity) as total_quantity_sold,
        sum(s.amount) as total_revenue,
        count(distinct s.customer_id) as unique_customers,
        count(distinct s.store_id) as stores_sold_in
    from sales s
    group by s.product_id
)

select
    p.product_id,
    p.product_name,
    p.category,
    p.base_price,
    coalesce(ps.times_sold, 0) as times_sold,
    coalesce(ps.total_quantity_sold, 0) as total_quantity_sold,
    coalesce(ps.total_revenue, 0) as total_revenue,
    coalesce(ps.unique_customers, 0) as unique_customers,
    coalesce(ps.stores_sold_in, 0) as stores_sold_in
from products p
left join product_sales ps on p.product_id = ps.product_id
