from sqlalchemy.orm.decl_api import DeclarativeBase
from ...._core import _BaseLylac
from ...._module_types import (
    DataPerRecord,
    ModelRecord,
    FieldAttributes,
    DataBaseDataType,
    TType,
)
from .._module_types import ColumnGenerator

class _BaseModels():

    build_column: dict[TType, ColumnGenerator]
    atts: list[str]

    def create_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def delete_model(
        self,
        model_name: str
    ) -> None:
        ...

    def add_field_to_model(
        self,
        table_model: type[DeclarativeBase],
        field: FieldAttributes,
    ) -> None:
        ...

    def build_field_atts(
        self,
        params: ModelRecord.BaseModelField,
    ) -> FieldAttributes:
        ...

class _BaseDatabase():

    def add_column(
        self,
        params: FieldAttributes
    ) -> None:
        ...

    def drop_column(
    self,
        table_name: str,
        column_name: str
    ) -> None:
        ...

class _BaseDDLManager():
    _main: _BaseLylac
    _model: _BaseModels
    _db: _BaseDatabase

    def new_table(
        self,
        name: str,
        sync_to_db: bool = False
    ) -> None:
        ...

    def new_field(
        self,
        model_name: str,
        params: ModelRecord.BaseModelField
    ) -> None:
        ...

    def delete_table(
        self,
        model_name: str,
    ) -> None:
        ...

    def delete_field(
        self,
        model_name: str,
        field_name: str
    ) -> None:
        ...

    def add_default_to_model(
        self,
        model_id: int,
        field_names: list[str] = []
    ) -> None:
        ...
