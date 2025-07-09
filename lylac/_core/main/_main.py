import pandas as pd
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    CriteriaStructure,
    RecordData,
    ModelName,
    OutputOptions,
    RecordValue,
)
from ..._core._env import ENV_VARIABLES
from .._interface import (
    Access_Interface,
    Algorythms_Interface,
    Auth_Interface,
    Automations_Interface,
    Compiler_Interface,
    Connection_Interface,
    DDL_Interface,
    DQL_Interface,
    Index_Interface,
    Metadata_Interface,
    Models_Interface,
    Output_Interface,
    Preprocess_Interface,
    Query_Interface,
    Select_Interface,
    Structure_Interface,
    Validations_Interface,
    Where_Interface,
)

class _Lylac_Core():
    _access: Access_Interface
    _algorythms: Algorythms_Interface
    _auth: Auth_Interface
    _automations: Automations_Interface
    _compiler: Compiler_Interface
    _connection: Connection_Interface
    _ddl: DDL_Interface
    _dql: DQL_Interface
    _index: Index_Interface
    _metadata: Metadata_Interface
    _models: Models_Interface
    _output: Output_Interface
    _preprocess: Preprocess_Interface
    _query: Query_Interface
    _select: Select_Interface
    _strc: Structure_Interface
    _validations: Validations_Interface
    _where: Where_Interface

    _base: type[DeclarativeBase]
    _engine: Engine

    _TOKEN = ENV_VARIABLES.CRYPT.ADMIN

    def create(
        self,
        token: str,
        model_name: ModelName,
        data: RecordData | list[RecordData],
    ) -> list[int]:
        ...

    def search(
        self,
        token: str,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[int]:
        ...

    def get_value(
        self,
        token: str,
        model_name: ModelName,
        record_id: int,
        field: str,
    ) -> RecordValue:
        ...

    def get_values(
        self,
        token: str,
        model_name: ModelName,
        record_id: int,
        fields: list[str],
    ) -> tuple:
        ...

    def read(
        self,
        token: str,
        model_name: ModelName,
        record_ids: int | list[int],
        fields: list[str] = [],
        sortby: str | list[str] = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | list[dict[str, RecordValue]]:
        ...

    def search_read(
        self,
        token: str,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
        fields: list[str] = [],
        offset: int | None = None,
        limit: int | None = None,
        sortby: str | list[str] | None = None,
        ascending: bool | list[bool] = True,
        output_format: OutputOptions | None = None,
        only_ids_in_relations: bool = False,
    ) -> pd.DataFrame | dict[str, RecordValue]:
        ...

    def search_count(
        self,
        token: str,
        model_name: ModelName,
        search_criteria: CriteriaStructure = [],
    ) -> int:
        ...

    def update(
        self,
        token: str,
        model_name: ModelName,
        record_ids: int | list[int],
        data: RecordData,
    ) -> bool:
        ...

    def update_where(
        self,
        token: str,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        data: RecordData,
        _record_ids: list[int] = []
    ) -> bool:
        ...

    def delete(
        self,
        token: str,
        model_name: ModelName,
        record_ids: int | list[int]
    ) -> bool:
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
