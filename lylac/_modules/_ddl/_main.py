from ..._constants import MODEL_NAME
from ..._core import _Lylac
from ..._data import default_field_template
from ..._module_types import (
    CriteriaStructure,
    ModelRecord,
    NewRecord,
)
from ._modules import (
    _Automations,
    _BaseDDLManager,
    _Database,
    _Models,
    _Reset
)

class DDLManager(_BaseDDLManager):

    def __init__(
        self,
        instance: _Lylac,
    ) -> None:

        # Asignación de la instancia propietaria
        self._main = instance
        # Referencia del motor de conexión
        self._engine = instance._engine
        # Creación del submódulo para operaciones en la base de datos
        self._db = _Database(self)
        # Creación del submódulo para operaciones en los modelos de SQLAlchemy
        self._model = _Models(self)
        # Creación del submódulo para operaciones de reseteo de base de datos
        self._reset = _Reset(self)
        # Creación del submódulo de automatizaciones
        self._automations = _Automations(self)

    def new_table(
        self,
        name: str,
    ) -> None:
        """
        ### Nueva tabla
        Este método realiza la declaración de un nuevo modelo de SQLAlchemy y realiza
        la creación de su respectiva tabla en la base de datos.
        """

        # Inicialización del modelo
        table_model = self._model.create_model(name)

        # Se crea el modelo como tabla en la base de datos
        table_model.__table__.create(self._main._engine)

    def new_field(
        self,
        model_name: str,
        params: ModelRecord.BaseModelField,
    ) -> None:

        # Obtención del modelo de SQLAlchemy
        model_model = self._main._strc.models[model_name]['model']

        # Creación de los parámetros para ser usados en las automatizaciones
        new_field = self._model.build_field_atts(params)

        # Se añade la columna al modelo SQLAlchemy de la tabla
        self._model.add_field_to_model(model_model, new_field)

        # Se añade la columna a la tabla de la base de datos
        self._db.add_column(new_field)

    def delete_table(
        self,
        model_name: str,
    ) -> None:

        # Obtención del modelo de SQLAlchemy
        model_model = self._main._strc.models[model_name]['model']

        # Se elimina la tabla de la base de datos
        model_model.__table__.drop(self._engine)

        # Se elimina el modelo
        self._model.delete_model(model_name)

    def delete_field(
        self,
        model_name: str,
        field_name: str,
    ) -> None:

        # Obtención de la ID del modelo
        [ model_id ] = self._main.search(MODEL_NAME.BASE_MODEL, [('model', '=', model_name)])

        # Creación de criterio de búsqueda para encontrar todos los campos pertenientes al modelo
        criteria: CriteriaStructure = [
            '&',
                '&',
                    ('model_id', '=', model_id),
                    ('name', '!=', field_name),
                ('name', 'not in', ['id', 'name', 'create_date', 'write_date']),
        ]

        # Se obtienen los datos de los registros a excepción del campo eliminado
        fields_data: list[ModelRecord.BaseModelField] = self._main.search_read(MODEL_NAME.BASE_MODEL_FIELD, criteria, output_format= 'dict')

        # Se crean las instancias de campos para ser añadidas
        fields_atts = [ self._model.build_field_atts(field) for field in fields_data ]

        # Obtención del nombre de la tabla
        table_name = self._main.get_value(MODEL_NAME.BASE_MODEL, model_id, 'name')

        # Se elimina la columna de la tabla de base de datos
        self._db.drop_column(table_name, field_name)

        # Se elimina el modelo de SQLAlchemy
        self._model.delete_model(model_name, table_name)

        # Se vuelve a crear el modelo
        table_model = self._model.create_model(table_name)

        # Se añaden los campos que tenía registrados
        for field in fields_atts:
            self._model.add_field_to_model(table_model, field)

    def add_default_to_model(
        self,
        model_id: int,
        field_names: list[str] = [],
    ) -> None:

        default_fields = ['create_uid', 'write_uid']
        complete_field_names = field_names + default_fields

        # Inicialización de la lista de datos a retornar
        fields_data: list[NewRecord.ModelField] = []

        # Creación de los datos por cada nombre de campo
        for field_name in complete_field_names:

            # Se obtiene una copia de la plantilla de información
            field_data = default_field_template[field_name].copy()

            # Se asigna la ID del modelo
            field_data['model_id'] = model_id

            # Se añaden los datos del campo a la lista de datos a retornar
            fields_data.append(field_data)

        # Se crea la información de los campos
        self._main.create(MODEL_NAME.BASE_MODEL_FIELD, fields_data)
