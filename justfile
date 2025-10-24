sync:
    uv sync --project data_generator
    uv sync --project orchestrator

generate-data:
    uv run --project data_generator python data_generator/generate_data.py

setup-ducklake:
    cd src_db && duckdb :memory: < setup.sql

setup-dbt:
    cd orchestrator/transforms && uv run --project .. dbt deps

setup: sync generate-data setup-ducklake setup-dbt

dbt-run:
    cd orchestrator/transforms && uv run --project .. dbt run

dagster-dev:
    cd orchestrator && uv run dagster dev

clean:
    rm -rf src_data/*.parquet
    rm -rf src_db/*.duckdb* src_db/*.ducklake*
    rm -rf dst_db/*.duckdb* dst_db/*.ducklake*
    cd orchestrator/transforms && uv run --project .. dbt clean