from typing import Tuple
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import (
    ModelMap,
    TType,
)
from ._base_base_lylac import BaseBaseLylac

class BaseStructure():
    models: dict[str, ModelMap]
    _main: BaseBaseLylac

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
        selection_values: list[str] = [],
    ) -> None:
        ...

    def unregister_field(
        self,
        model_name: str,
        field_name: str,
    ) -> None:
        ...

    def register_relation(
        self,
        model_model: type[DeclarativeBase],
    ) -> None:
        ...

    def update_selection_values(
        self,
        model_name: str,
        field_name: str,
        selection_values: list[str],
    ) -> None:
        ...

    def get_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def get_relation_model(
        self,
        model_name: str,
        field_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def get_model_names(
        self,
    ) -> list[str]:
        ...

    def get_model_field_names(
        self,
        model_name: str,
    ) -> list[str]:
        ...

    def get_related_model_name(
        self,
        model_name: str,
        field_name: str,
    ) -> str:
        ...

    def get_related_field_name(
        self,
        model_name: str,
        field_name: str,
    ) -> str:
        ...

    def get_relation_model_name(
        self,
        model_name: str,
        field_name: str,
    ) -> str:
        ...

    def get_field_ttype(
        self,
        model_name: str,
        field_name: str,
    ) -> TType:
        ...

    def get_table_name(
        self,
        model_name: str,
    ) -> str:
        ...

    def get_ttype_fields(
        self,
        model_name: str,
        ttype: TType,
    ) -> list[str]:
        ...

    def get_field_selection_values(
        self,
        model_name: str,
        field_name: str,
    ) -> list[str]:
        ...

    def initialize_fields_atts(
        self,
    ) -> None:
        ...
