set dotenv-filename := 'orchestrator/.env'

setup-env:
    touch orchestrator/.env
    echo "DAGSTER_HOME=$(pwd)/orchestrator/dagster_home" >> orchestrator/.env

setup-uv:
    uv sync --project data_generator
    uv sync --project orchestrator
    uv sync --project orchestrator/dbt_project

setup-data:
    uv run --project data_generator python data_generator/generate_data.py

setup-dbt:
    cd orchestrator/dbt_project && uv run dbt deps

setup-dagster:
    mkdir -p $DAGSTER_HOME

setup-ducklake:
    cd src_db && duckdb :memory: < setup.sql

setup: setup-uv setup-dbt setup-dagster setup-data setup-ducklake

inspect:
    @echo "=== Source Database (DuckLake) ==="
    duckdb :memory: -c "ATTACH 'ducklake:src_db/metadata.ducklake' AS metadata; SHOW TABLES FROM metadata;"
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

clean-artifacts:
    rm -rf src_data/*.parquet
    rm -rf src_db/*.duckdb* src_db/*.ducklake*
    rm -rf dst_db/*.duckdb* dst_db/*.ducklake*
    cd orchestrator/dbt_project && uv run dbt clean
    rm -rf $DAGSTER_HOME

clean-envs:
    rm -rf **/.venv
    rm -rf **/uv.lock

destroy: clean-artifacts clean-envs

rebuild: destroy setup inspect