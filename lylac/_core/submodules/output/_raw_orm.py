from typing import Callable
import pandas as pd
from sqlalchemy import select, and_
from ...._module_types import (
    TType,
    ModelName,
)

class _RawORM_Interface():

    def get_fields_ttypes(
        self,
        model_name: ModelName,
        fields: list[str],
    ) -> dict[str, TType]:
        ...
