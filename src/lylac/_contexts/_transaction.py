from typing import Generic
from .._contexts import ExecutionContext
from .._contexts.engines import BaseContext
from .._resources import ModelDataIndex
from .._typing.type_parameters import _M

class TransactionContext(Generic[_M], BaseContext[_M]):

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
    ) -> None:

        # Asignación de valores
        self._execution_ctx = execution_ctx
        self._crud = execution_ctx._crud
        self.conn = execution_ctx.conn

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)
