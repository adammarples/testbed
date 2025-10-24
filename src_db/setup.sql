INSTALL ducklake;
ATTACH 'ducklake:metadata.ducklake' AS metadata;
USE metadata;

CREATE OR REPLACE TABLE raw_customers AS
FROM read_parquet('src_data/raw_customers.parquet');

CREATE OR REPLACE TABLE raw_stores AS
FROM read_parquet('src_data/raw_stores.parquet');

CREATE OR REPLACE TABLE raw_products AS
FROM read_parquet('src_data/raw_products.parquet');

CREATE OR REPLACE TABLE raw_sales AS
FROM read_parquet('src_data/raw_sales.parquet');
