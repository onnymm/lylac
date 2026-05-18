from datetime import datetime
from typing import Any
from typing import Literal
from typing import Generic
from typing import Optional
from typing import overload
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ..._typing.callables import ComputeFieldFn
from ..._typing.literals import AggFuncName
from ..._typing.literals import TTypeName
from ..._typing.structures import ComputeContextHub
from ..._typing.type_parameters import _M
from ..._typing.type_parameters import _M

class Contract_ComputeContext(Generic[_M]):
    _hub: ComputeContextHub[_M]
    """Centro de funciones de cómputo de campos."""

    @overload
    def __getitem__(
        self,
        field_name: Literal['id'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['name'],
    ) -> InstrumentedAttribute[str]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['create_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['update_date'],
    ) -> InstrumentedAttribute[datetime]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['create_uid'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['update_uid'],
    ) -> InstrumentedAttribute[int]:
        ...
    @overload
    def __getitem__(
        self,
        field_name: Literal['display_name'],
    ) -> InstrumentedAttribute[str]:
        ...
    def concat(
        self,
        *args: tuple[Any],
    ) -> InstrumentedAttribute[str]:
        ...
    def case(
        self,
        *args: tuple[BinaryExpression, Any],
        default: Any = None,
    ) -> InstrumentedAttribute:
        ...
    def cast(
        self,
        field_name_or_instance: str | InstrumentedAttribute,
        ttype: TTypeName,
    ) -> InstrumentedAttribute:
        ...
    def agg(
        self,
        o2m_field_name: str,
        field_to_aggregate_name: str | ComputeFieldFn[_M],
        fn_name: AggFuncName,
        search_criteria: list = [],
        default_zero_value: Optional[str | int | float] = None,
    ) -> InstrumentedAttribute:
        ...
    def weekday(
        self,
        field: str | InstrumentedAttribute,
    ) -> InstrumentedAttribute:
        ...
