from typing import (
    Any,
)
from sqlalchemy.sql.selectable import Select
from ..._module_types import (
    TTypesMapping,
    ModelName,
)

class BaseSelect():

    def build(
        self,
        model_name: ModelName,
        fields: list[str] = [],
    ) -> tuple[Select[Any], TTypesMapping]:
        ...
