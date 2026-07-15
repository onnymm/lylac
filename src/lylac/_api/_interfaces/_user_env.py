from typing import Generic
from ..._engines import UserEnvEngine
from ..._typing.callables import LazyResolver
from ..._typing.generics import FunctionDecorator
from ..._typing.type_parameters import _M

class _Interface_UserEnv(Generic[_M]):

    def __init__(
        self,
        engine: UserEnvEngine[_M],
    ) -> None:

        # Asignación de valores
        self._engine = engine

    def register_value(
        self,
        value_name: str,
    ) -> FunctionDecorator[LazyResolver[_M]]:

        # Construcción de decorador para registro de función
        decorator = self._engine.register(value_name)

        return decorator
