from typing import Callable
from typing import Generic
from ..._engines import ValidationEngine
from ..._typing.callables import ValidationCallback
from ..._typing.generics import ItemOrList
from ..._typing.generics import ModelName
from ..._typing.literals import DMLTransaction
from ..._typing.type_parameters import _M

class _Interface_Validations(Generic[_M]):
    _core: ValidationEngine[_M]

    def __init__(
        self,
        validations: ValidationEngine[_M],
    ) -> None:

        # Asignación de motor de validaciones
        self._core = validations

    def register(
        self,
        on: ItemOrList[DMLTransaction],
        model_name: ModelName[_M],
        message: str,
    ) -> Callable[[ValidationCallback[_M]], ValidationCallback[_M]]:

        decorator = self._core.register(
            on,
            model_name,
            message,
        )

        return decorator
