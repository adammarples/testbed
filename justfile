sync:
    uv sync --project data_generator
    uv sync --project orchestrator
    uv sync --project orchestrator/dbt_project

generate-data:
    uv run --project data_generator python data_generator/generate_data.py

setup-ducklake:
    cd src_db && duckdb :memory: < setup.sql

setup-dbt:
    cd orchestrator/dbt_project && uv run dbt deps

setup: sync generate-data setup-ducklake setup-dbt

inspect:
    @echo "=== Source Database (DuckLake) ==="
    uv run --project src_db duckdb :memory: -c "ATTACH 'ducklake:src_db/metadata.ducklake' AS metadata; SHOW TABLES FROM metadata;"
    @echo "\n=== Destination Database (Analytics) ==="
    duckdb dst_db/analytics.duckdb -c "SHOW TABLES;"
    @echo "\n=== dbt Configuration ==="
    cd orchestrator/dbt_project && uv run dbt debug
    @echo "\n=== dbt Models ==="
    cd orchestrator/dbt_project && uv run dbt ls
    @echo "\n=== Dagster Assets ==="
    cd orchestrator && uv run dagster asset list -m dagster_project

dbt-run:
    cd orchestrator/dbt_project && uv run dbt run

dagster-dev:
    cd orchestrator && uv run dagster dev

clean:
    rm -rf src_data/*.parquet
    rm -rf src_db/*.duckdb* src_db/*.ducklake*
    rm -rf dst_db/*.duckdb* dst_db/*.ducklake*
    cd orchestrator/dbt_project && uv run dbt clean
    rm -rf orchestrator/.dagster_home

clean-envs:
    rm -rf **/.venv
    rm -rf **/uv.lock

rebuild: clean clean-envs setup inspect