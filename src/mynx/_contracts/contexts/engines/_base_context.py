from typing import Generic
from typing import Literal
from typing import Optional
from ...._resources import ModelDataIndex
from ...._typing.generics import ItemOrList
from ...._typing.generics import MaybeNone
from ...._typing.generics import ModelName
from ...._typing.generics import _Record
from ...._typing.structures import CriteriaStructure
from ...._typing.structures import FieldReadDeclaration
from ...._typing.type_parameters import _M

class Contract_BaseContext(Generic[_M]):
    model_data_index: ModelDataIndex

    @property
    def uid(
        self,
    ) -> int:
        ...

    def create(
        self,
        model_name: ModelName[_M],
        data: ItemOrList[dict],
    ) -> list[int]:
        ...

    def search(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:
        ...

    def read(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ) -> list[_Record]:
        ...

    def search_read(
        self,
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
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:
        ...

    def update(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        data: dict,
    ) -> Literal[True]:
        ...

    def get_resource_id(
        self,
        ref: str,
    ) -> MaybeNone[int]:
        ...
