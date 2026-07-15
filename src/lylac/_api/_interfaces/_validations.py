from typing import Callable
from typing import Generic
from ..._engines import ValidationEngine
from ..._typing.callables import ValidationCallback
from ..._typing.generics import ItemOrList
from ..._typing.generics import ModelName
from ..._typing.literals import DMLTransaction
from ..._typing.type_parameters import _M

class _Interface_Validations(Generic[_M]):
    _engine: ValidationEngine[_M]

    def __init__(
        self,
        engine: ValidationEngine[_M],
    ) -> None:

        # Asignación de motor de validaciones
        self._engine = engine

    def register(
        self,
        on: ItemOrList[DMLTransaction],
        model_name: ModelName[_M],
        message: str,
    ) -> Callable[[ValidationCallback[_M]], ValidationCallback[_M]]:

        # Obtención del decorador para registrar la función
        decorator = self._engine.register(
            on,
            model_name,
            message,
        )

        return decorator
