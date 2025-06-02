from ...._core import _BaseLylac
from ...._module_types import (
    DataPerRecord,
    ModelRecord,
    NewField,
    DataBaseDataType,
    TType,
)
from .._module_types import ColumnGenerator

class _BaseModels():

    build_column: dict[TType, ColumnGenerator]

    def delete_model(
        self,
        model_name: str
    ) -> None:
        ...

class _BaseDatabase():

    def drop_column(
    self,
        table_name: str,
        column_name: str
    ) -> None:
        ...

class _BaseDDLManager():
    _class_ttype: dict[TType, DataBaseDataType]
    _main: _BaseLylac
    _model: _BaseModels
    _db: _BaseDatabase

    def _create_table(
        self,
        name: str,
        sync_to_db: bool = False
    ) -> None:
        ...

    def _add_column_to_model(
        self,
        params: NewField
    ) -> None:
        ...

    def _add_column_to_db(
        self,
        params: NewField
    ) -> None:
        ...

    def _parse_default_value(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField]
    ) -> (int | float | str | bool | None):
        ...

    def _prepare_column_data(
        self,
        params: DataPerRecord
    ) -> NewField:
        ...
