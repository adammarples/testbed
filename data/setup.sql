INSTALL ducklake;
ATTACH 'ducklake:lake.ducklake' AS lake;
USE lake;

CREATE SCHEMA IF NOT EXISTS raw;

CREATE OR REPLACE TABLE raw.raw_customers AS
FROM read_parquet('generated_data/raw_customers.parquet');

CREATE OR REPLACE TABLE raw.raw_stores AS
FROM read_parquet('generated_data/raw_stores.parquet');

CREATE OR REPLACE TABLE raw.raw_products AS
FROM read_parquet('generated_data/raw_products.parquet');

CREATE OR REPLACE TABLE raw.raw_sales AS
FROM read_parquet('generated_data/raw_sales.parquet');
