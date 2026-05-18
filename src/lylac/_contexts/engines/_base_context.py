from typing import Generic
from typing import Literal
from typing import Optional
from ..._contracts import _Contract_CRUD
from ..._contracts.contexts import Contract_ExecutionContext
from ..._contracts.contexts.engines import Contract_BaseContext
from ..._resources import ModelDataIndex
from ..._typing.generics import ItemOrList
from ..._typing.generics import MaybeNone
from ..._typing.generics import ModelName
from ..._typing.generics import _Record
from ..._typing.structures import CriteriaStructure
from ..._typing.structures import RecordData
from ..._typing.structures import FieldReadDeclaration
from ..._typing.type_parameters import _M

class BaseContext(Generic[_M], Contract_BaseContext[_M]):
    _model_data_index: ModelDataIndex
    _execution_ctx: Contract_ExecutionContext[_M]
    _crud: _Contract_CRUD[_M]

    @property
    def uid(
        self,
    ) -> int:
        """
        ID del usuario que ejecuta la transacción.
        """

        # Obtención de la ID del usuario en la ejecución
        uid = self._execution_ctx.uid

        return uid

    def create(
        self,
        model_name: ModelName[_M],
        data: ItemOrList[RecordData],
    ) -> list[int]:

        # Creación de registros y obtención de sus IDs
        created_ids = self._crud.create(
            self._execution_ctx,
            model_name,
            data,
        )

        return created_ids

    def search(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:

        # Búsqueda de registros
        record_ids = self._crud.search(
            self._execution_ctx,
            model_name,
            search_criteria,
            offset,
            limit,
        )

        return record_ids

    def read(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ) -> list[_Record]:

        # Obtención de los datos
        records_data = self._crud.read(
            self._execution_ctx,
            model_name,
            record_ids,
            fields,
            sortby,
            ascending,
        )

        return records_data

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

        # Obtención de los datos
        records_data = self._crud.search_read(
            self._execution_ctx,
            model_name,
            search_criteria,
            fields,
            offset,
            limit,
            sortby,
            ascending,
        )

        return records_data

    def search_count(
        self,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure = [],
    ) -> int:

        # Obtención del conteo de resultados
        count = self._crud.search_count(
            self._execution_ctx,
            model_name,
            search_criteria,
        )

        return count

    def update(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        data: RecordData,
    ) -> Literal[True]:

        # Modificación de los registros
        result = self._crud.update(
            self._execution_ctx,
            model_name,
            record_ids,
            data,
        )

        return result

    def delete(
        self,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
    ) -> Literal[True]:

        # Eliminación de los registros
        result = self._crud.delete(
            self._execution_ctx,
            model_name,
            record_ids,
        )

        return result

    def get_resource_id(
        self,
        ref: str,
    ) -> MaybeNone[int]:

        # Obtención de la ID de recurso
        resource_id = self._model_data_index.get_resource_id(ref)

        return resource_id
