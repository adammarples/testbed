set dotenv-filename := 'orchestrator/.env'

setup-env:
    touch orchestrator/.env
    echo "DAGSTER_HOME={{justfile_directory()}}/orchestrator/.dagster_home" >> orchestrator/.env

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

setup-minio:
    @mkdir -p data/minio/ducklake-data
    just start-minio

start-minio:
    @minio server data/minio --console-address ":9001" > /dev/null 2>&1 & echo $$! > /tmp/minio.pid
    @echo "MinIO started in background (PID: `cat /tmp/minio.pid`)"
    @echo "Web console: http://localhost:9001 (user: minioadmin, pass: minioadmin)"

stop-minio:
    @pkill -f "minio server data/minio" || echo "MinIO not running"
    @rm -f /tmp/minio.pid

setup-ducklake:
    cd data && duckdb host.duckdb < setup.sql

setup: setup-uv setup-dbt setup-dagster setup-data setup-minio setup-ducklake

inspect-dbt:
    cd orchestrator/dbt_project && uv run dbt debug && uv run dbt ls

inspect-minio:
    @tree data/minio/ducklake-data/

inspect-ducklake:
    duckdb data/host.duckdb -c "ATTACH 'ducklake:data/lakehouse.ducklake' AS lake(DATA_PATH 's3://ducklake-data/data/'); SHOW ALL TABLES;"

inspect-dagster:
    cd orchestrator && uv run dagster asset list -m dagster_project

inspect: inspect-minio inspect-ducklake inspect-dbt inspect-dagster

dbt-run:
    cd orchestrator/dbt_project && uv run dbt run

serve:
    cd orchestrator && uv run dagster dev

clean-artifacts:
    rm -rf data/**/*.parquet
    rm -rf data/*.duckdb* data/*.ducklake*
    rm -rf data/minio/
    cd orchestrator/dbt_project && uv run dbt clean
    rm -rf $DAGSTER_HOME

clean-envs:
    rm -rf **/.venv
    rm -rf **/uv.lock

destroy: stop-minio clean-artifacts clean-envs

rebuild: destroy setup inspect