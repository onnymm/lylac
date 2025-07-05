from ...._contexts import Context
from ...._core import BaseAutomations
from ...._module_types import (
    DataPerRecord,
    ModelRecordData,
)

class _Automations():

    def __init__(
        self,
        instance: BaseAutomations,
    ):

        # Asignación de la clase propietaria
        self._automations = instance

    def register_new_model(
        self,
        ctx: Context.Individual[ModelRecordData.BaseModel_],
        # params: DataPerRecord[ModelRecordData.BaseModel_],
    ) -> None:

        self._automations.register_model(ctx.data['model'])
