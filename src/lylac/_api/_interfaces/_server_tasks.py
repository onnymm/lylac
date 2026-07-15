from typing import Generic
from ..._engines import ServerTasksEngine
from ..._typing.callables import ServerTaskCallback
from ..._typing.generics import FunctionDecorator
from ..._typing.type_parameters import _M

class _Interface_ServerTasks(Generic[_M]):
    _engine: ServerTasksEngine[_M]

    def __init__(
        self,
        engine: ServerTasksEngine[_M],
    ) -> None:

        # Asignación de motor de tareas de servidor
        self._engine = engine

    def register(
        self,
        name: str,
    ) -> FunctionDecorator[ServerTaskCallback[_M]]:

        # Obtención del decorador para registrar la función
        decorator = self._engine.register(name)

        return decorator
