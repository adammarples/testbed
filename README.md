# Data Testbed Project

A demonstration project for learning the interactions between DuckLake, dbt, and Dagster. Disclaimer: 90% vibe-coded.

## Requirements
* uv
* duckdb >= 1.2
* just

```bash
brew install uv duckdb just
```

## Quick Start

```bash
# Run once to create a required .env file
just setup-env

# Install dependencies, generate data and set up warehouse
just setup

# Inspect all your data and assets
just inspect

# Run dbt transformations
just dbt-run

# Start Dagster UI
just dagster-dev

# Nuke envs, data, logs, state, rebuild and inspect all
just rebuild

```

## Architecture

```mermaid
graph LR
    subgraph "Data Generation"
        A[data_generator]
        B[src_data/*.parquet]
    end

    subgraph "DuckLake Warehouse"
        C[raw_customers<br/>raw_stores<br/>raw_products<br/>raw_sales]
    end

    subgraph "Dagster Orchestration"
        subgraph "dbt Transforms"
            D[Staging Layer<br/>stg_customers<br/>stg_stores<br/>stg_products<br/>stg_sales]
            E[Metrics Layer<br/>customer_metrics<br/>store_metrics<br/>product_metrics]
        end
    end

    A -->|generates| B
    B -->|loaded into| C
    C -->|source tables| D
    D -->|aggregates| E

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style D fill:#e1f5ff,stroke:#0288d1,stroke-width:2px
    style E fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
```

## Components

### data_generator
Generates synthetic retail data (customers, stores, products, sales) as parquet files.

### src_db
DuckLake warehouse storing source data with:
- `raw_customers` - customer dimension with SCD2 history
- `raw_stores` - store dimension with SCD2 history
- `raw_products` - product catalog
- `raw_sales` - sales transactions

### orchestrator/dbt_project
dbt project that transforms source data into:
- **Staging layer**: Clean views of raw tables
- **Metrics layer**: Aggregated business metrics (customer lifetime value, store performance, product analytics)

### orchestrator/dagster_project
Dagster code that orchestrates the dbt transformations.


## Tech Stack

- **DuckDB** - embedded analytical database
- **DuckLake** - lakehouse format built on DuckDB
- **dbt** - data transformation framework
- **Dagster** - data orchestration platform
- **uv** - Python package manager
- **just** - command runner
