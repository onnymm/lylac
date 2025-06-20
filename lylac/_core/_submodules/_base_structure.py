from typing import (
    Literal,
    Tuple,
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    DBCredentials,
    CriteriaStructure,
    ModelMap,
    RecordData,
    DataOutput,
    OutputOptions,
    RecordValue,
    TType,
)
from ._base_base_lylac import BaseBaseLylac

class BaseStructure():
    models: dict[str, ModelMap]
    _main: BaseBaseLylac

    def get_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def register_table(
        self,
        table_instance: type[DeclarativeBase],
    ) -> None:
        ...

    def unregister_table(
        self,
        table_name: str,
    ) -> None:
        ...

    def register_field(
        self,
        model_name: str,
        field_name: str,
        ttype: TType,
        relation: str | None,
    ) -> None:
        ...

    def unregister_field(
        self,
        model_name: str,
        field_name: str,
    ) -> None:
        ...

    def initialize_fields_atts(
        self,
    ) -> None:
        ...

    def get_fields_atts(
        self,
        model_name: str,
        fields: list[str] = [],
    ) -> list[Tuple[str, TType, str | None]]:
        ...
