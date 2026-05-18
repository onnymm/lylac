from typing import Any
from typing import Generator
from typing import Generic
from typing import Optional
from typing import TYPE_CHECKING
from sqlalchemy import Subquery
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression
from ..._resources import FieldProperties
from ..._resources import FieldTarget
from ..._resources import OuterJoin
from ..._typing.aliases import ModelClass
from ..._typing.generics import ModelName
from ..._typing.type_parameters import _M
from ..._typing.structures import FieldReadDeclaration

if TYPE_CHECKING:
    from ._where import Contract_WhereContext

class Contract_FrameContext(Generic[_M]):
    model_name: ModelName[_M]
    origin_model: ModelClass

    @property
    def outerjoins(
        self,
    ) -> tuple[OuterJoin]:
        ...

    def create_field_target(
        self,
        field_read_declaration: FieldReadDeclaration,
        only_id_for_m2o: bool = False,
    ) -> FieldTarget[_M]:
        ...

    def create_filter_context(
        self,
    ) -> 'Contract_WhereContext[_M]':
        ...

    def portal(
        self,
        model_name: ModelName[_M],
    ) -> Contract_FrameContext[_M]:
        ...

    def spawn_relative(
        self,
        path: str,
    ) -> Contract_FrameContext[_M]:
        ...

    def get_field_instances_from_target(
        self,
        field_target: FieldTarget[_M],
    ) -> list[InstrumentedAttribute]:
        ...

    def get_field_instances(
        self,
        field_complete_name: str,
        field_label: Optional[str] = None,
    ) -> list[InstrumentedAttribute]:
        ...

    def get_physical_field_instance_from_current(
        self,
        field_name: str,
    ) -> InstrumentedAttribute:
        ...

    def get_database_model_names(
        self,
    ) -> Generator[ModelName[_M], Any, None]:
        ...


    def get_field_properties(
        self,
        model_name: ModelName[_M],
        field_name: str,
    ) -> FieldProperties[_M]:
        ...

    def get_aliased_model_model(
        self,
        model_name: ModelName[_M],
    ) -> ModelClass:
        ...

    def get_physical_field_instance(
        self,
        source: ModelClass | Subquery,
        field_name: str,
    ) -> InstrumentedAttribute:
        ...

    def is_reference_field(
        self,
        field_reference_or_name: str,
    ) -> bool:
        ...

    def get_path_and_name(
        self,
        field_reference: str,
    ) -> tuple[str, str]:
        ...

    def add_outerjoin(
        self,
        model: ModelClass,
        on: BinaryExpression
    ) -> None:
        ...
