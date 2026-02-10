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
    cd orchestrator/dbt_project && if [ -f packages.yml ]; then uv run dbt deps; fi

setup-dagster:
    mkdir -p $DAGSTER_HOME

setup-rustfs:
    @mkdir -p data/rustfs/ducklake-data
    just start-rustfs

start-rustfs:
    @rustfs data/rustfs --address :9000 --access-key rustfsadmin --secret-key rustfsadmin > /dev/null 2>&1 & echo $$! > /tmp/rustfs.pid
    @echo "rustfs started in background (PID: `cat /tmp/rustfs.pid`)"
    @echo "S3 API: http://localhost:9000 (access key: rustfsadmin, secret key: rustfsadmin)"

stop-rustfs:
    @pkill -f "rustfs data/rustfs" || echo "rustfs not running"
    @rm -f /tmp/rustfs.pid

setup-ducklake:
    cd data && duckdb host.duckdb < setup.sql

setup: setup-uv setup-dbt setup-dagster setup-data setup-rustfs setup-ducklake

inspect-dbt:
    cd orchestrator/dbt_project && uv run dbt debug && uv run dbt ls

inspect-rustfs:
    find data/rustfs/ducklake-data/ -type f

inspect-ducklake:
    duckdb data/host.duckdb -c "ATTACH 'ducklake:data/lakehouse.ducklake' AS lake(DATA_PATH 's3://ducklake-data/'); SHOW ALL TABLES;"

inspect-dagster:
    cd orchestrator && uv run dagster asset list -m dagster_project

inspect: inspect-rustfs inspect-ducklake inspect-dbt inspect-dagster

dbt-run:
    cd orchestrator/dbt_project && uv run dbt run

serve:
    cd orchestrator && uv run dagster dev

clean-artifacts:
    rm -rf data/**/*.parquet
    rm -rf data/*.duckdb* data/*.ducklake*
    rm -rf data/rustfs/
    cd orchestrator/dbt_project && uv run dbt clean
    rm -rf $DAGSTER_HOME

clean-envs:
    find . -type d -name ".venv" -exec rm -rf {} +
    find . -type f -name "uv.lock" -exec rm -f {} +

destroy: stop-rustfs clean-artifacts clean-envs

rebuild: destroy setup inspect