from typing import Any
from typing import Generic
from typing import Optional
from typing import TYPE_CHECKING
from .._contexts.engines import BaseContext
from .._resources import ErrorDetail
from .._resources import ModelDataIndex
from .._typing.generics import ModelName
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._orchestrator import CRUD

class PoliciesContext(Generic[_M, _R], BaseContext[_M]):

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
        crud: CRUD[_M],
        model_name: ModelName[_M],
        records: list[_R],
        errors: list[ErrorDetail],
        message: str,
    ) -> None:

        # Asignación de valores
        self.model_name = model_name
        self.records = records
        self._crud = crud
        self._message = message
        self._errors = errors
        self._execution_ctx = execution_ctx

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)

    def catch(
        self,
        record: _R,
        value: Optional[Any] = None,
        data: Optional[Any] = None,
        show_error_data: bool = True,
    ) -> None:

        # Construcción de mensaje a mostrar
        message_to_show = self._message.format(value= value, data= data)
        # Inicialización de detalle de error
        detail = ErrorDetail(value, record, message_to_show, show_error_data)
        # Se añade el registro como error
        self._errors.append(detail)
