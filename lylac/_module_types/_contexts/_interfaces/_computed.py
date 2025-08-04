from typing import Any
from ...._core.main import _Lylac_Core
from ..._base_categories import (
    CriteriaStructure,
    ModelName,
    AggFunctionName,
)
from ._select import _SelectContextCore
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression

class _ComputeContextCore():

    def __init__(
        self,
        model_name: ModelName,
        select_context: _SelectContextCore,
        lylac_instance: _Lylac_Core,
    ) -> None:
        ...

    def __getitem__(
        self,
        field_name: str,
    ) -> InstrumentedAttribute[Any]:
        ...

    def case(
        self,
        *args: tuple[BinaryExpression, Any],
        default: Any,
    ) -> InstrumentedAttribute:
        ...

    def agg(
        self,
        composed_field_name: str,
        aggregation_function: AggFunctionName,
        search_criteria: CriteriaStructure = [],
    ) -> InstrumentedAttribute:
        ...
