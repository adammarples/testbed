from pathlib import Path
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

# Path to dbt project
DBT_PROJECT_DIR = Path(__file__).parent.parent / "transforms"
DBT_PROFILES_DIR = DBT_PROJECT_DIR

# Create dbt project instance
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
)

# Create dbt resource
transforms_resource = DbtCliResource(project_dir=str(DBT_PROJECT_DIR), profiles_dir=str(DBT_PROFILES_DIR))


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_transforms(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    dbt models for transforming source data into staging and metrics.
    """
    yield from dbt.cli(["build"], context=context).stream()
