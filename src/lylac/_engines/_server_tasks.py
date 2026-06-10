from typing import Generic
from typing import Literal
from typing import TYPE_CHECKING
from .._constants import ERROR_LABEL
from .._contexts import ServerTaskContext as _ServerTaskContext
from .._data import PRESET_SERVER_TASKS
from .._resources import ServerTaskProperties
from .._typing.callables import ServerTaskCallback
from .._typing.callables import ActionCallback
from .._typing.generics import FunctionDecorator
from .._typing.type_parameters import _M
from ..errors import SeverTaskExecutionError

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._orchestrator import CRUD

class ServerTasksEngine(Generic[_M]):

    def __init__(
        self,
        crud: CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        # Inicialización de centro de acciones
        self._hub: dict[str, ServerTaskProperties[_M]] = PRESET_SERVER_TASKS.copy()

    def register(
        self,
        name: str,
    ) -> FunctionDecorator[ServerTaskCallback[_M]]:

        # Inicialización de decorador para obtener la función a registrar
        def decorator(callback: ServerTaskCallback[_M]):

            # Registro de la tarea
            self._register_task(name, callback)

            # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
            replaced_function = self._build_void_function()

            return replaced_function

        return decorator

    def execute(
        self,
        execution_ctx: ExecutionContext[_M],
        name: str,
    ) -> Literal[True]:

        # Obtención de las propiedades
        task_properties = self._hub[name]
        # Obtención de la función
        task_callback = task_properties.callback
        # Inicialización de contexto de tarea
        ctx = _ServerTaskContext[_M](execution_ctx, self._crud)
        # Ejecución de la tarea
        task_callback(ctx)

    def _register_task(
        self,
        name: str,
        callback: ServerTaskCallback[_M],
    ) -> None:

        # Inicialización de propiedades de la tarea
        task_properties = ServerTaskProperties[_M](name, callback)

        self._hub[name] = task_properties

    def _build_void_function(
        self,
    ) -> FunctionDecorator[ActionCallback[_M]]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(ctx: ActionCallback[_M]) -> None:
            # Se lanza error de ejecución
            raise SeverTaskExecutionError(ERROR_LABEL.MANUAL_SERVER_TASK)

        return void_function
