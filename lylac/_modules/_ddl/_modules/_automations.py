from ...._constants import MODEL_NAME
from ...._data import base_fields
from ...._module_types import (
    DataPerRecord,
    ModelRecord,
)
from ._base import _BaseDDLManager

class _Automations():

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia de la instancia principal
        self._main = instance._main
        # Referencia del motor de conexión
        self._engine = instance._main._engine
        # Referencia del módulo de modelos
        self._model = instance._model
        # Referencia de la estructura interna de tablas
        self._strc = instance._main._strc

    def create_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        # Creación de la tabla en la base de datos
        self._ddl.new_table(params.record_data['name'])

    def create_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> None:

        # Obtención del nombre del modelo
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['model_id'], 'model')

        # Se añade el campo a la tabla indicada
        self._ddl.new_field(model_name, params.record_data)

    def delete_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        # Ejecución del método del módulo principal
        self._ddl.delete_table(params.record_data['model'])

    def delete_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField]
    ) -> None:

        # Obtención del nombre del modelo
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['model_id'], 'model')

        # Ejecución del método del módulo principal
        self._ddl.delete_field(model_name, params.record_data['name'])

    def create_base_fields(
        self,
        params: DataPerRecord[ModelRecord.BaseModel]
    ) -> None:
        
        # Inicialización de los datos
        fields_data: list[ModelRecord.BaseModelField] = []

        # Se crea la información
        for base_field in base_fields:

            # Se crea una copia de la información
            field_data = base_field.copy()

            # Se añade la ID del modelo a vincular
            field_data['model_id'] = params.id

            # Se añade la información a la lista de datos
            fields_data.append(field_data)

        # Se crean los registros en la tabla de campos
        self._main.create('base.model.field', fields_data)

    def add_preset_fields(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        # Obtención de la ID del modelo
        model_id = params.id

        # Se añaden los campos predeterminados
        self._ddl._model.add_default_fields_to_model(model_id)
