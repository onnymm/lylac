from typing import Generic
from typing import TYPE_CHECKING
from .._contexts.engines import BaseContext
from .._resources import ModelDataIndex
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._orchestrator import CRUD
    from .._contexts import ExecutionContext

class ServerTaskContext(Generic[_M], BaseContext[_M]):

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
        crud: CRUD[_M],
    ) -> None:

        self._execution_ctx = execution_ctx
        self._crud = crud
        self._model_data_index = ModelDataIndex(execution_ctx.conn)
