from ..._core import _Lylac
from ..._module_types import Transaction
from ..._constants import MESSAGES

class Access():

    def __init__(
        self,
        instance: _Lylac
    ) -> None:

        # Asignación de instancia principal
        self._main = instance
        # Referencia de la instancia de autenticación
        self._auth = instance._auth

    def check_permission(
        self,
        user_id: int,
        transaction: Transaction,
    ) -> None:

        # Revisión de permiso de transacción
        granted = self._main._compiler.check_permission(user_id, transaction)

        # Si el usuario no tiene permiso de realiza la acción se arroja un error
        if not granted:
            raise PermissionError(MESSAGES.ACCESS.NOT_ALLOWED)
