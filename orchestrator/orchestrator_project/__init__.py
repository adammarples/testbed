from dagster import Definitions
from .assets import dbt_transforms, transforms_resource

defs = Definitions(
    assets=[dbt_transforms],
    resources={
        "dbt": transforms_resource,
    },
)
