from pathlib import Path
from dagster import AssetExecutionContext, Definitions, DefaultScheduleStatus, define_asset_job, ScheduleDefinition
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject, DagsterDbtTranslator


DBT_PROJECT_DIR = Path(__file__).parent.parent / "dbt_project"
DBT_PROFILES_DIR = DBT_PROJECT_DIR

dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR.as_posix(),
    profiles_dir=DBT_PROFILES_DIR.as_posix(),
)

dbt_cli = DbtCliResource(
    project_dir=dbt_project.project_dir,
    profiles_dir=dbt_project.profiles_dir,
)


@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=DagsterDbtTranslator(), # enables asset checks for dbt tests
)
def dbt_transforms(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    dbt models for transforming source data into staging and metrics.
    """
    yield from dbt.cli(["build"], context=context).stream()


dbt_job = define_asset_job(name="dbt_job")

daily_dbt_schedule = ScheduleDefinition(
    job=dbt_job,
    cron_schedule="*/2 * * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)

# main entrypoint for dagster
defs = Definitions(
    assets=[dbt_transforms],
    resources={"dbt": dbt_cli},  # "dbt" key here is significant, it maps to the dbt parameter in the asset function
    jobs=[dbt_job],
    schedules=[daily_dbt_schedule],
)
