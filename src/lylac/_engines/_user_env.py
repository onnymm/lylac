from typing import Generic
from typing import TYPE_CHECKING
from .._constants import ERROR_LABEL
from .._typing.callables import LazyResolver
from .._typing.type_parameters import _M
from ..errors import VariableResolverExecutionError

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._orchestrator import CRUD

class UserEnvEngine(Generic[_M]):

    def __init__(
        self,
        crud: CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        # Inicialización de diccionario de resolución
        self._resolvers: dict[str, LazyResolver[_M]] = {}

    def register(
        self,
        name: str,
    ):

        # Inicialización de decorador para obtener la función a registrar
        def decorator(callback: LazyResolver[_M]) -> LazyResolver[_M]:

            # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
            replaced_function = self._build_void_function()

            # Registro de la función proporcionada
            self._resolvers[name] = callback

            return replaced_function

        return decorator

    def _build_void_function(
        self,
    ) -> LazyResolver[_M]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(callback: ExecutionContext[_M]) -> None:
            # Se lanza error de ejecución
            raise VariableResolverExecutionError(ERROR_LABEL.MANUAL_ACTION)

        return void_function
