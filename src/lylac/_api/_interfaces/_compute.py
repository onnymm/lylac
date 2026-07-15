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
    _engine: ComputeEngine[_M]

    def __init__(
        self,
        engine: ComputeEngine[_M],
        main: Lylac[_M],
    ) -> None:

        self._engine = engine
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
            execution_ctx = self._main._create_execution_context(DATA_RESOURCE.ROOT_USER, conn)

            # Obtención del decorador para registrar la función
            closure_decorator = self._engine.register_field(
                self._main._crud,
                execution_ctx,
                model_name,
                name,
                label,
                ttype,
            )

            return closure_decorator

        # Obtención de decorador comstruido
        decorator = self._main._engine.execute_complex(transaction)

        return decorator
