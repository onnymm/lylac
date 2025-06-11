from sqlalchemy import (
    Select,
    asc,
    desc,
)
from sqlalchemy.orm.decl_api import DeclarativeBase
from ..._core import _Lylac
from ..._module_types import _T

class Query():

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance

        # Inicialización de mapa de direcciones de ordenamiento
        self._build_sorting_directions_map()

    def build_sort(
        self,
        stmt: Select[_T],
        table_instance: DeclarativeBase,
        sortby: str | list[str],
        ascending: str | list[bool],
    ) -> Select[_T]:

        # Ordenamiento de los datos
        if sortby is None:
            # Ordenamiento de los datos por IDs
            stmt = stmt.order_by( asc( getattr(table_instance, 'id') ) )

        elif isinstance(sortby, str):
            # Creación del query
            stmt = stmt.order_by(
                # Obtención de función de ordenamiento
                self._sorting_direction[ascending](
                    # Obtención del campo atributo de la tabla
                    getattr(table_instance, sortby)
                )
            )

        # Ordenamiento por varias columnas
        elif isinstance(sortby, list):
            stmt = stmt.order_by(
                # Destructuración en [*args] de una compreensión de lista
                *[
                    # Obtención de función de ordenamiento
                    self._sorting_direction[ascending_i](
                        # Obtención del campo atributo de la tabla
                        getattr(table_instance, sortby_i)
                    )
                    # Destructuración de la columna y dirección de ordenamiento del zip de listas
                    for ( sortby_i, ascending_i ) in zip(
                        sortby, ascending
                    )
                ]
            )

        return stmt

    def build_segmentation(
        self,
        stmt: Select[_T],
        offset: int | None = None,
        limit: int | None = None,
    ) -> Select[_T]:

        # Segmentación de inicio y fin en caso de haberlos
        if offset != None:
            stmt = stmt.offset(offset)
        if limit != None:
            stmt = stmt.limit(limit)

        # Retorno del query
        return stmt

    def _build_sorting_directions_map(
        self,
    ) -> None:

        self._sorting_direction = {
            True: asc,
            False: desc,
        }
