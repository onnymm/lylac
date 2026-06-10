from typing import Generic
from typing import TYPE_CHECKING
from .._constants import FIELD_NAME
from .._resources import ModelDataIndex
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R
from .engines import BaseContext

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._operations import DDL
    from .._orchestrator import CRUD

class ActionContext(Generic[_M, _R], BaseContext[_M]):
    data: _R
    record_id: int

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
        crud: CRUD[_M],
        record: _R,
        ddl: DDL[_M],
    ) -> None:

        # Asignación de valores
        self.data = record
        self.record_id = record[FIELD_NAME.ID]
        self._execution_ctx = execution_ctx
        self._crud = crud
        self._ddl = ddl

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)
