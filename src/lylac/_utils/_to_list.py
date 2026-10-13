from typing import Iterable
from .._typing.generics import ScalarOrIterable
from .._typing.type_parameters import _T

def to_list(
    content: ScalarOrIterable[_T],
) -> list[_T]:

    # El contenido es un iterable
    is_iterable = isinstance(content, Iterable)
    # El contenido no es un diccionario
    not_dict = not isinstance(content, dict)
    # El contenido no es un string
    not_string = not isinstance(content, str)

    # Si el contenido cumple con las condiciones
    if is_iterable and not_dict and not_string:
        # Se retorna igual
        return list(content)
    # Se retorna el contenido dentro de una lista
    return [content]
