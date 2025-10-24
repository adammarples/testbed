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
    cd data && duckdb lakehost.duckdb < setup.sql

setup: setup-uv setup-dbt setup-dagster setup-data setup-ducklake

inspect:
    @echo "=== ALl Tables (DuckLake) ==="
    duckdb data/lakehost.duckdb -c "ATTACH 'ducklake:data/lake.ducklake'; SHOW ALL TABLES;"
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
    rm -rf data/**/*.parquet
    rm -rf data/*.duckdb* data/*.ducklake*
    cd orchestrator/dbt_project && uv run dbt clean
    rm -rf $DAGSTER_HOME

clean-envs:
    rm -rf **/.venv
    rm -rf **/uv.lock

destroy: clean-artifacts clean-envs

rebuild: destroy setup inspect