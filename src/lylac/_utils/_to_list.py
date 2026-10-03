from typing import Iterable
from .._typing.generics import ScalarOrIterable
from .._typing.type_parameters import _T

def to_list(
    content: ScalarOrIterable[_T],
) -> list[_T]:

    # Si el contenido ya es un iterable pero no un diccionario...
    if isinstance(content, Iterable) and not isinstance(content, dict):
        # Se retorna igual
        return list(content)
    # Se retorna el contenido dentro de una lista
    return [content]
