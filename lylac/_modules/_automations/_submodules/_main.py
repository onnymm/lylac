from ...._module_types import (
    DataPerRecord,
    ModelRecord,
)
from ...._core import BaseAutomations

class _Automations():

    def __init__(
        self,
        instance: BaseAutomations,
    ):

        # Asignación de la clase propietaria
        self._automations = instance

    def register_new_model(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        self._automations.register_model(params.record_data['model'])
