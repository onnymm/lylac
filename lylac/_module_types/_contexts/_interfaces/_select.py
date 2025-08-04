from typing import Any
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ..._base_categories import TType

class _SelectContextCore():

    def __init__(
        self,
    ) -> None:
        ...

    def add_field_instance(
        self,
        field_instance: InstrumentedAttribute[Any],
    ) -> None:
        ...

    def add_ttype_mapping(
        self,
        field_name: str,
        ttype: TType,
    ) -> None:
        ...

    def add_outerjoin(
        self,
        model_model: type[DeclarativeBase],
        binary_expression: BinaryExpression,
    ) -> None:
        ...
