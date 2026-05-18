from typing import Generic
from typing import Literal
from typing import Optional
from .._contracts.contexts import Contract_ExecutionContext
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.structures import CriteriaStructure
from .._typing.structures import RecordData
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M

class _Contract_CRUD(Generic[_M]):
    def create(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        data: ItemOrList[RecordData],
    ) -> list[int]:
        ...
    def search(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:
        ...
    def search_read(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:
        ...
    def search_count(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:
        ...
    def read(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ) -> list[_Record]:
        ...
    def update(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        data: RecordData,
    ) -> Literal[True]:
        ...
    def delete(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
    ) -> Literal[True]:
        ...
