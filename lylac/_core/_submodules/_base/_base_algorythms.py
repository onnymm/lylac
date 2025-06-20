from typing import (
    Callable,
    TypeVar,
    overload,
)

# Tipo de dato entrante
_T = TypeVar('_T')
# Tipo de dato extraído del tipo entrante
_E = TypeVar('_E')
# Tipo de dato para clasificación
_C = TypeVar('_C')

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
