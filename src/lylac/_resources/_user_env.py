from typing import Any
from typing import Generic
from typing import TYPE_CHECKING
from .._typing.callables import LazyResolver
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._contexts import ExecutionContext

class UserEnv(Generic[_M]):

    def __init__(
        self,
        execution_ctx: ExecutionContext[_M],
        resolvers: dict[str, 'LazyResolver[_M]'],
    ) -> None:

        # Asignación de valores
        self._execution_ctx = execution_ctx
        self._resolvers = resolvers
        # IKnicialización de diccionario de variables memoizadas
        self._memo = {}

    def __getitem__(
        self,
        name: str,
    ) -> Any:

        # Si el valor solicitado ya se encuentra memoizado...
        if name in self._memo:
            # Se usa éste
            return self._memo[name]

        # Obtención de la función de resolución de valor
        resolution_fn = self._resolvers[name]
        try:
            # Obtención del valor
            value = resolution_fn(self._execution_ctx)
        except Exception:
            # Se retorna un None
            value = None

        # Memoización del valor
        self._memo[name] = value

        return value
