from typing import Optional
from ..._constants import FIELD_NAME
from ..._module_types import (
    CriteriaStructure,
    ModelName,
)
from ..._core.main import _Lylac_Core
from ..._core.modules import DQL_Core

class DQLManager(DQL_Core):

    def __init__(
        self,
        instance: _Lylac_Core,
    ) -> None:

        # Asignación del módulo principal
        self._main = instance
        # Asignación de la instancia de conexión
        self._connection = instance._connection
        # Asignación de la instancia de manejo de formato de salida
        self._output = instance._output
        # Asignación de la instancia query
        self._query = instance._query
        # Asignación de la instancia de SELECT
        self._select = instance._select
        # Asignación de la instancia de estructura interna
        self._strc = instance._strc
        # Asígnación de la instancia WHERE
        self._where = instance._where

    def search(
        self,
        model_name: ModelName,
        search_criteria: CriteriaStructure,
        offset: Optional[int],
        limit: Optional[int],
    ) -> list[int]:

        # Creación del query SELECT
        ( stmt, _ ) = self._select.build(model_name, [FIELD_NAME.ID])
        # Obtención de la instancia de la tabla
        model_model = self._strc.get_model(model_name)

        # Si hay criterios de búsqueda se genera el WHERE
        if len(search_criteria) > 0:
            # Creación del query WHERE
            where_query = self._where.build_where(model_model, search_criteria)
            # Conversión del Query SQL
            stmt = stmt.where(where_query)

        # Ordenamiento de los datos
        stmt = self._query.build_sort(stmt, model_model, FIELD_NAME.ID, True)
        # Segmentación de inicio y fin en caso de haberlos
        stmt = self._query.build_segmentation(stmt, offset, limit)
        # Ejecución de la transacción
        response = self._connection.execute(stmt)
        # Obtención de las IDs encontradas
        found_ids = self._output.get_found_ids(response)

        return found_ids
