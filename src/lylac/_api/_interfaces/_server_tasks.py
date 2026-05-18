from typing import Generic
from ..._engines import ServerTasksEngine
from ..._typing.callables import ServerTaskCallback
from ..._typing.generics import FunctionDecorator
from ..._typing.type_parameters import _M

class _Interface_ServerTasks(Generic[_M]):
    _core: ServerTasksEngine[_M]

    def __init__(
        self,
        server_tasks: ServerTasksEngine[_M],
    ) -> None:

        # Asignación de motor de tareas de servidor
        self._core = server_tasks

    def register(
        self,
        name: str,
    ) -> FunctionDecorator[ServerTaskCallback[_M]]:

        decorator = self._core.register(name)

        return decorator
