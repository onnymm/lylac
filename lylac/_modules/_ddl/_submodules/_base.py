from sqlalchemy.orm.decl_api import DeclarativeBase
from ...._core import _Lylac
from ...._module_types import (
    FieldDefinition,
    ModelRecord,
    TType,
)
from .._module_types import ColumnGenerator

class _BaseModels():

    build_column: dict[TType, ColumnGenerator]
    """
    ### Construcción de columna
    Este mapa de métodos construye una columna tipada para un modelo de SQLALchemy.
    Uso:
    >>> # Creación de un campo tipo 'integer'
    >>> field = NewField(...)
    >>> column = self.build_column['integer'](field)
    """

    def create_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def create_relation(
        self,
        owner_model_name: str,
        referenced_model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def delete_model(
        self,
        model_name: str,
    ) -> None:
        ...

    def add_field_to_model(
        self,
        model_model: type[DeclarativeBase],
        field: FieldDefinition,
    ) -> None:
        ...

    def build_field_atts(
        self,
        params: ModelRecord.BaseModelField,
    ) -> FieldDefinition:
        ...

class _BaseDatabase():

    def add_column(
        self,
        params: FieldDefinition
    ) -> None:
        ...

    def drop_column(
    self,
        table_name: str,
        column_name: str
    ) -> None:
        ...

class _BaseDDLManager():
    _main: _Lylac
    _m_model: _BaseModels
    _m_db: _BaseDatabase

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

    def new_relation(
        self,
        owner_model_name: str,
        referenced_model_name: str,
    ) -> None:
        ...

    def delete_relation(
        self,
        model_name: str,
        field_name: str,
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
