from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    CriteriaStructure,
    RecordData,
    CredentialsAlike,
    DataOutput,
    OutputOptions,
    RecordValue,
)
from ._base import (
    BaseAlgorythms,
    BaseConnection,
    BaseModels,
)

class BaseBaseLylac():
    _algorythms: BaseAlgorythms
    _base: type[DeclarativeBase]
    _credentials: CredentialsAlike
    _connection: BaseConnection
    _engine: Engine
    _model_template: type[DeclarativeBase]
    _models: BaseModels

    def create(
        self,
        table_name: str,
        data: RecordData | list[RecordData],
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
        self,
        table_name: str,
        record_ids: int | list[int],
        fields: list[str] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> DataOutput:
        ...

    def get_value(
        self,
        table_name: str,
        record_id: int,
        field: str,
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
        only_ids_in_relations: bool = False,
    ) -> DataOutput:
        ...

    def update(
        self,
        table_name: str,
        record_ids: int | list[int],
        data: RecordData,
    ) -> bool:
        ...

    def update_where(
        self,
        table_name: str,
        search_criteria: CriteriaStructure,
        data: RecordData,
    ) -> bool:
        ...

    def delete(
        self,
        table_name: str,
        record_ids: int | list[int]
    ) -> bool:
        ...

    def and_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure,
    ) -> CriteriaStructure:
        ...

    def or_(
        self,
        cs_1: CriteriaStructure,
        cs_2: CriteriaStructure,
    ) -> CriteriaStructure:
        ...
