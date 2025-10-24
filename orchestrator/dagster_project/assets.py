from pathlib import Path
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject, DagsterDbtTranslator

# Path to dbt project
DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"
DBT_PROFILES_DIR = DBT_PROJECT_DIR

# Create dbt project instance
dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
)

# Create dbt resource
dbt_resource = DbtCliResource(project_dir=str(DBT_PROJECT_DIR), profiles_dir=str(DBT_PROFILES_DIR))

# Create translator to enable asset checks for dbt tests
dagster_dbt_translator = DagsterDbtTranslator()


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=dagster_dbt_translator,
)
def dbt_transforms(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    dbt models for transforming source data into staging and metrics.
    """
    yield from dbt.cli(["build"], context=context).stream()
