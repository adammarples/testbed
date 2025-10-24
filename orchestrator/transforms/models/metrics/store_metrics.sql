with sales as (
    select * from {{ ref('stg_sales') }}
),

stores as (
    select * from {{ ref('stg_stores') }}
    where is_current = true
),

store_sales as (
    select
        s.store_id,
        count(distinct s.transaction_id) as total_sales,
        count(distinct s.customer_id) as unique_customers,
        sum(s.amount) as total_revenue,
        avg(s.amount) as avg_sale_amount,
        min(s.sale_date) as first_sale_date,
        max(s.sale_date) as last_sale_date
    from sales s
    group by s.store_id
)

select
    st.store_id,
    st.store_name,
    st.location,
    st.store_type,
    st.opened_date,
    coalesce(ss.total_sales, 0) as total_sales,
    coalesce(ss.unique_customers, 0) as unique_customers,
    coalesce(ss.total_revenue, 0) as total_revenue,
    coalesce(ss.avg_sale_amount, 0) as avg_sale_amount,
    ss.first_sale_date,
    ss.last_sale_date
from stores st
left join store_sales ss on st.store_id = ss.store_id
