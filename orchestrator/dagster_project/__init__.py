from dagster import Definitions
from .assets import dbt_transforms, dbt_resource

defs = Definitions(
    assets=[dbt_transforms],
    resources={
        "dbt": dbt_resource,
    },
)
