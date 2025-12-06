INSTALL ducklake;
INSTALL aws;
LOAD aws;

CREATE OR REPLACE PERSISTENT SECRET (
    TYPE S3,
    ENDPOINT 'localhost:9000',
    USE_SSL false,
    URL_STYLE 'path',
    REGION 'us-east-1',
    KEY_ID 'rustfsadmin',
    SECRET 'rustfsadmin'
);

ATTACH 'ducklake:lakehouse.ducklake' AS lake(DATA_PATH 's3://ducklake-data/');
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
