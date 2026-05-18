from .._typing.generics import ItemOrList
from .._typing.type_parameters import _T

def to_list(
    content: ItemOrList[_T],
) -> list[_T]:

    # Si el contenido ya es una lista...
    if isinstance(content, list):
        # Se retorna igual
        return content
    # Se retorna el contenido dentro de una lista
    return [content]
