from typing import (
    Callable,
    overload,
)
from ...._module_types import (
    _C,
    _E,
    _T,
)

class BaseAlgorythms():

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E] = lambda value: value,
        groupby: None = None,
    ) -> list[_E]:
        ...

    @overload
    def find_duplicates(
        self,
        data: list[_T],
        extractor: Callable[[_T], _E],
        groupby: Callable[[_T], _C],
    ) -> dict[_C, list[_E]]:
        ...
