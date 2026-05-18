from typing import Generic
from ..._engines import ActionEngine
from ..._typing.callables import ActionCallback
from ..._typing.generics import FunctionDecorator
from ..._typing.generics import ModelName
from ..._typing.type_parameters import _M

class _Interface_Actions(Generic[_M]):
    _core: ActionEngine[_M]

    def __init__(
        self,
        actions: ActionEngine[_M],
    ) -> None:

        # Asignación de motor de acciones
        self._core = actions

    def register(
        self,
        model_name: ModelName[_M],
        name: str,
    ) -> FunctionDecorator[ActionCallback[_M]]:

        decorator = self._core.register(
            model_name,
            name,
        )

        return decorator
