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
        self._model = instance._m_model
        # Referencia de la estructura interna de tablas
        self._strc = instance._main._strc

    def create_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo creado
        model_name = params.record_data['name']
        # Creación de la tabla en la base de datos
        self._ddl.new_table(model_name)

    def create_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> None:

        # Obtención de la ID del modelo del campo creado
        model_id = params.record_data['model_id']
        # Obtención del nombre del modelo
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Se añade el campo a la tabla indicada
        self._ddl.new_field(model_name, params.record_data)

    def delete_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_],
    ) -> None:

        # Obtención del nombre del modelo
        model_name = params.record_data['model']
        # Ejecución del método del módulo principal
        self._ddl.delete_table(model_name)

    def delete_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField]
    ) -> None:

        # Obtención de la ID del modelo del campo creado
        model_id = params.record_data['model_id']
        # Obtención del nombre del modelo
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, model_id, 'model')
        # Obtención del nombre del campo
        field_name = params.record_data['name']
        # Ejecución del método del módulo principal
        self._ddl.delete_field(model_name, field_name)

    def create_relation_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> None:

        # Nombre del modelo propietario
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['model_id'], 'model')
        # Nombre del modelo referenciado
        related_model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['related_model_id'], 'model')
        # Creación de la tabla de relación
        self._ddl.new_relation(model_name, related_model_name)

    def delete_relation_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> None:

        # Nombre del modelo propietario
        model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, params.record_data['model_id'], 'model')
        # Nombre del campo
        field_name = params.record_data['name']

        # Se elimina la tabla de relación
        self._ddl.delete_relation(model_name, field_name)

    def create_base_fields(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_]
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
        self._main.create(MODEL_NAME.BASE_MODEL_FIELD, fields_data)

    def add_preset_fields(
        self,
        params: DataPerRecord[ModelRecord.BaseModel_],
    ) -> None:

        # Obtención de la ID del modelo
        model_id = params.id
        # Se añaden los campos predeterminados
        self._ddl.add_default_to_model(model_id)
