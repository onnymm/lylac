from typing import (
    Any,
    Literal,
)
from sqlalchemy.sql.selectable import Select, TypedReturnsRows
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeBase
from .._module_types import DBCredentials
from .._module_types import (
    _T,
    CriteriaStructure,
    RecordData,
    DataOutput,
    OutputOptions,
    RecordValue,
)
from sqlalchemy.orm.attributes import InstrumentedAttribute

class _BaseStructure():
    models: dict[str, type[DeclarativeBase]]

    def register_table(
        self,
        table_instance: type[DeclarativeBase],
    ) -> None:
        ...

    def unregister_table(
        self,
        table_name: str
    ) -> None:
        ...

class _BaseModels():

    def get_table_model(
        self,
        table_name: str
    ) -> type[DeclarativeBase]:
        ...

    def get_id_field(
        self,
        table_model: type[DeclarativeBase]
    ) -> InstrumentedAttribute[int]:
        ...

    def get_table_field(
        self,
        table: str,
        field: str
    ) -> InstrumentedAttribute:
        ...

    def get_table_fields(
        self,
        table_instance: type[DeclarativeBase],
        fields: list[str] = [],
        include_id: bool = True
    ) -> list[InstrumentedAttribute[Any]]:
        ...

class _BaseConnection():

    def execute(
        self,
        statement: Select[_T] | TypedReturnsRows[_T],
        commit: bool = False
    ) -> CursorResult[_T]:
        ...

    def create_connection(
        self,
        credentials: DBCredentials | str | Literal['env']
    ) -> Engine:
        ...

class _BaseLylac():
    credentials: Literal['env'] | DBCredentials | str = 'env',
    _strc: _BaseStructure
    _base: type[DeclarativeBase]
    _engine: Engine
    _models: _BaseModels
    _connection: _BaseConnection

    def create(
    self,
    table_name: str,
    data: RecordData | list[RecordData]
) -> list[int]:
        ...

    def search(
        self,
        table_name: str,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:
        ...

    def read(
        table_name: str,
        record_ids: int | list[int],
        fields: list[str] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None
    ) -> DataOutput:
        ...

    def get_value(
        self,
        table_name: str,
        record_id: int,
        field: str
    ) -> RecordValue:
        ...

    def get_values(
        self,
        table_name: str,
        record_id: int,
        fields: list[str]
    ) -> tuple:
        ...

    def search_read(
        self,
        table_name: str,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
    ) -> DataOutput:
        ...

    def _get_table_field(
        self,
        table: str,
        field: str
    ) -> InstrumentedAttribute:
        ...

    def and_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:
        ...

    def or_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure
    ) -> CriteriaStructure:
        ...
