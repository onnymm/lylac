from typing import Any
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.decl_api import DeclarativeBase

class BaseModels():

    def get_table_model(
        self,
        model_name: str,
    ) -> type[DeclarativeBase]:
        ...

    def get_id_field(
        self,
        model_model: type[DeclarativeBase],
    ) -> InstrumentedAttribute[int]:
        ...

    def get_table_field(
        self,
        model_model: type[DeclarativeBase],
        field: str,
    ) -> InstrumentedAttribute:
        ...

    def get_table_fields(
        self,
        model_model: type[DeclarativeBase],
        fields: list[str] = [],
        include_id: bool = True,
    ) -> list[InstrumentedAttribute[Any]]:
        ...
