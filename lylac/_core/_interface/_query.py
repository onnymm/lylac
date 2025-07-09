from sqlalchemy import Select
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._module_types import _T

class Query_Interface():

    def build_sort(
        self,
        stmt: Select[_T],
        model_model: type[DeclarativeBase],
        sortby: str | list[str],
        ascending: str | list[bool],
    ) -> Select[_T]:
        ...

    def build_segmentation(
        self,
        stmt: Select[_T],
        offset: int | None = None,
        limit: int | None = None,
    ) -> Select[_T]:
        ...
