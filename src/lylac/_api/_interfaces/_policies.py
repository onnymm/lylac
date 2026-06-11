from typing import Callable
from typing import Generic
from typing import TYPE_CHECKING
from ..._typing.callables import PolicyCallback
from ..._typing.generics import ItemOrList
from ..._typing.generics import ModelName
from ..._typing.literals import DMLTransaction
from ..._typing.type_parameters import _M

if TYPE_CHECKING:
    from ..._engines import PoliciesEngine

class _Interface_Policies(Generic[_M]):
    _core: PoliciesEngine[_M]

    def __init__(
        self,
        engine: PoliciesEngine[_M],
    ) -> None:

        # Asignación de motor de validaciones
        self._core = engine

    def register(
        self,
        on: ItemOrList[DMLTransaction],
        model_name: ModelName[_M],
        message: str,
    ) -> Callable[[PolicyCallback[_M]], PolicyCallback[_M]]:

        decorator = self._core.register(
            on,
            model_name,
            message,
        )

        return decorator
