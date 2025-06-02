from ...._module_types import (
    DataPerRecord,
    ModelRecord,
)
from ._base import _BaseAutomations

class _Automations():

    def __init__(
        self,
        instance: _BaseAutomations,
    ):

        # Asignación de la clase propietaria
        self._automations = instance

    def register_new_model(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        self._automations._register_model(params.record_data['model'])
