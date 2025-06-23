from ...._constants import MODEL_NAME
from ...._module_types import (
    DataPerRecord,
    ModelRecord,
)
from ...._core import BaseValidations

class _Automations():

    def __init__(
        self,
        instance: BaseValidations,
    ) -> None:

        # Asignación de instancia propietaria
        self._validations = instance
        # Asignación de instancia principal
        self._main = instance._main

    def initialize_validations(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_],
    ) -> None:

        # Ejecución de inicialización de validaciones de modelo
        self._validations.initialize_model_validations(params.record_data['model'])

    def delete_validations(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_],
    ) -> None:

        # Ejecución de eliminación de validaciones de modelo
        self._validations.drop_model_validations(params.record_data['model'])
