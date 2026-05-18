from typing import Generic
from .._contracts import _Contract_CRUD
from .._contracts.contexts import Contract_ExecutionContext
from .._resources import ModelDataIndex
from .._typing.generics import ModelName
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R
from .engines import BaseContext

class AutomationContext(Generic[_M, _R], BaseContext[_M]):
    records: list[_R]

    def __init__(
        self,
        records: list[_R],
        execution_ctx: Contract_ExecutionContext[_M],
        crud: _Contract_CRUD[_M],
        ddl: ...
    ) -> None:

        # Asignación de valores
        self.records = records
        self._execution_ctx = execution_ctx
        self._crud = crud
        self._ddl = ddl

        # Inicialización de índice de datos de modelo
        self._model_data_index = ModelDataIndex(execution_ctx.conn)

    def register_model(
        self,
        model_name: ModelName[_M],
    ) -> None:

        # Se añade el modelo en los motores
        self._execution_ctx.automations.add(model_name)
        self._execution_ctx.compute.add(model_name)
        self._execution_ctx.validations.add(model_name)
        self._execution_ctx.actions.add(model_name)
