from typing import Generic
from ..._engines import ActionEngine
from ..._typing.callables import ActionCallback
from ..._typing.generics import FunctionDecorator
from ..._typing.generics import ModelName
from ..._typing.type_parameters import _M

class _Interface_Actions(Generic[_M]):
    _engine: ActionEngine[_M]

    def __init__(
        self,
        engine: ActionEngine[_M],
    ) -> None:

        # Asignación de motor de acciones
        self._engine = engine

    def register(
        self,
        model_name: ModelName[_M],
        name: str,
        fields: list[str] = [],
    ) -> FunctionDecorator[ActionCallback[_M]]:

        # Obtención del decorador para registrar la función
        decorator = self._engine.register(
            model_name,
            name,
            fields,
        )

        return decorator
