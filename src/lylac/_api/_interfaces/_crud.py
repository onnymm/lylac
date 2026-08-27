from typing import Generic
from typing import TYPE_CHECKING
from ..._typing.callables import ProcessingCallback
from ..._typing.type_parameters import _A
from ..._typing.type_parameters import _M

if TYPE_CHECKING:
    from ..._orchestrator import CRUD

class _Interface_CRUD(Generic[_M]):
    _crud: 'CRUD[_M]'

    def __init__(
        self,
        engine: 'CRUD[_M]',
    ) -> None:

        # Asignación de orquestador
        self._crud = engine

    def register_on_creation_processing(
        self,
        processing_callbacks: list[ProcessingCallback[_A]],
    ) -> None:

        # Asignación de lista de funciones de preprocesamiento en creación
        self._crud.register_on_creation_processing(processing_callbacks)

    def register_on_update_processing(
        self,
        processing_callbacks: list[ProcessingCallback[_A]],
    ) -> None:

        # Asignación de lista de funciones de preprocesamiento en modificación
        self._crud.register_on_update_processing(processing_callbacks)
