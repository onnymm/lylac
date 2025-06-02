from ...._module_types import (
    CriteriaStructure,
    DataPerRecord,
    ModelRecord,
    NewField,
)
from ._base import _BaseDDLManager
from ...._data import base_fields

class _Automations():

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Referencia del módulo principal
        self._main = instance._main
        # Asignación de la instancia propietaria
        self._ddl = instance
        # Referencia de la estructura interna de tablas
        self._strc = instance._main._strc

    def create_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField],
    ) -> None:

        # Creación de los parámetros para ser usados en las automatizaciones
        new_field = self._ddl._prepare_column_data(params)

        # Se añade la columna al modelo SQLAlchemy de la tabla
        self._ddl._add_column_to_model(new_field)

        # Se añade la columna a la tabla de la base de datos
        self._ddl._add_column_to_db(new_field)

    def create_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        # Creación de la tabla en la base de datos
        self._ddl._create_table(params.record_data['name'])

    def delete_table(
        self,
        params: DataPerRecord[ModelRecord.BaseModel],
    ) -> None:

        # Nombre del modelo
        model_name = params.record_data['model']
        # Nombre de la tabla
        table_name = params.record_data['name']

        # Obtención de la instancia del modelo de SQLAlchemy
        table_instance = self._strc.models[table_name]

        # Se elimina la tabla de la base de datos
        table_instance.__table__.drop(self._main._engine)

        # Se elimina el modelo de SQLAlchemy
        self._ddl._model.delete_model(model_name)

    def create_base_fields(
        self,
        params: DataPerRecord[ModelRecord.BaseModel]
    ) -> None:

        # Se añade la ID del modelo a vincular
        for field in base_fields:
            field['model_id'] = params.id

        # Se crean los registros en la tabla de campos
        self._main.create('base.model.field', base_fields)

    def delete_column(
        self,
        params: DataPerRecord[ModelRecord.BaseModelField]
    ) -> None:

        criteria: CriteriaStructure = [
            '&',
                ('model_id', '=', params.record_data['model_id']),
                ('name', 'not in', ['id', 'name', 'create_date', 'write_date']),
        ]

        # Se obtienen los datos de los registros
        records_data = self._main.search_read('base.model.field', criteria, output_format= 'dict')

        table_name = self._main.get_value('base.model', params.record_data['model_id'], 'name')

        new_fields = [ DataPerRecord(id= record_data['id'], record_data= record_data) for record_data in records_data ]

        # Se elimina el modelo de SQLAlchemy
        self._ddl._model.delete_model(table_name)

        # Se elimina la columna de la tabla de la base de datos
        self._ddl._db.drop_column(table_name, params.record_data['name'])

        # Se vuelve a crear el modelo
        self._ddl._create_table(table_name, sync_to_db= False)

        print(new_fields)

        # Se añaden las columnas
        for new_field in new_fields:
            data = self._ddl._prepare_column_data(new_field)
            self._ddl._add_column_to_model(data)
