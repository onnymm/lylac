from sqlalchemy import text
from ...._module_types import (
    FieldDefinition,
    TType,
)

class _Database_Interface():

    def add_column(
        self,
        params: FieldDefinition,
    ) -> None:
        ...

    def drop_column(
        self,
        table_name: str,
        column_name: str,
    ) -> None:
        ...
