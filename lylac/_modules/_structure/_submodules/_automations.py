from ...._constants import MODEL_NAME
from ...._contexts import Context
from ...._core import BaseStructure
from ...._module_types import (
    DataPerRecord,
    ModelRecordData,
)

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
        ctx: Context.Individual[ModelRecordData.BaseModelField],
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Obtención del nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['model_id'], 'model')

        # Inicialización del modelo de relación como nulo
        related_model = None
        related_field = None

        # Si existe una ID relacionada, se obtiene el nombre del modelo relacionado
        if ctx.data['related_model_id'] is not None:
            related_model = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['related_model_id'], 'model')
            related_field = ctx.data['related_field']

        # Registro del campo
        self._strc.register_field(
            model_name,
            ctx.data['name'],
            ctx.data['ttype'],
            related_model,
            related_field,
        )

    def unregister_fields_atts(
        self,
        ctx: Context.Individual[ModelRecordData.BaseModelField],
        # params: DataPerRecord[ModelRecordData.BaseModelField],
    ) -> None:

        # Obtención del nombre del modelo propietario
        model_name = ctx.get_value(MODEL_NAME.BASE_MODEL, ctx.data['model_id'], 'model')
        # Obtención del nombre del campo
        field_name = ctx.data['name']

        self._strc.unregister_field(model_name, field_name)
