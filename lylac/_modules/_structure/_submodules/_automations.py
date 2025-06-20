from ...._module_types import (
    DataPerRecord,
    ModelRecord,
)
from ...._constants import MODEL_NAME
from ...._core import BaseStructure

class _Automations():

    def __init__(
        self,
        instance: BaseStructure,
    ) -> None:

        # Asignación de la instancia propietaria
        self._strc = instance
        # Asignación de la instancia principal
        self._main = instance._main

    def register_field_atts(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField]
    ) -> None:

        # Obtención del nombre del modelo propietario
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['model_id'], 'model')

        # Inicialización del modelo de relación como nulo
        field_relation = None

        # Si existe una ID relacionada, se obtiene el nombre del modelo relacionado
        if params.record_data['related_model_id'] is not None:
            field_relation = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['related_model_id'], 'model')

        # Registro del campo
        self._strc.register_field(
            model_name,
            params.record_data['name'],
            params.record_data['ttype'],
            field_relation,
        )
