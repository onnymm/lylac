from typing import Generic
from typing import TYPE_CHECKING
from sqlalchemy.engine import Connection
from ..._constants import DATA_RESOURCE
from ..._engines import ComputeEngine
from ..._typing.generics import ModelName
from ..._typing.literals import TTypeName
from ..._typing.type_parameters import _M

if TYPE_CHECKING:
    from ..._main import Lylac

class _Interface_Compute(Generic[_M]):
    _core: ComputeEngine[_M]

    def __init__(
        self,
        computed: ComputeEngine[_M],
        main: Lylac[_M],
    ) -> None:

        self._core = computed
        self._main = main

    def register_field(
        self,
        model_name: ModelName[_M],
        name: str,
        label: str,
        ttype: TTypeName,
    ):

        # Definición de la transacción
        def transaction(conn: Connection):
            # Inicialización de contexto de ejecución
            execution_ctx = self._main._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)

            # Registro de campo en la instancia
            closure_decorator = self._core.register_field(
                self._main._crud,
                execution_ctx,
                model_name,
                name,
                label,
                ttype,
            )

            return closure_decorator

        # Obtención de decorador comstruido
        decorator = self._main._connection.execute_complex(transaction)

        return decorator
