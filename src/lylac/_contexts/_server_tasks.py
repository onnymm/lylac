from typing import Generic
from .._contexts.engines import BaseContext
from .._contracts import _Contract_CRUD
from .._contracts.contexts import Contract_ExecutionContext
from .._resources import ModelDataIndex
from .._typing.type_parameters import _M


class ServerTaskContext(Generic[_M], BaseContext[_M]):

    def __init__(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        crud: _Contract_CRUD[_M],
    ) -> None:

        self._execution_ctx = execution_ctx
        self._crud = crud
        self._model_data_index = ModelDataIndex(execution_ctx.conn)
