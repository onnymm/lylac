from sqlalchemy.exc import ProgrammingError
from ...._constants import (
    MESSAGES,
    MODEL_NAME,
)
from ...._data import (
    base_user,
    initial_data,
)
from ...._errors import InitializationError
from ._base import _BaseDDLManager

class _Reset():

    def __init__(
        self,
        instance: _BaseDDLManager,
    ) -> None:

        # Se inicializa estado de inicialización en falso
        self._state = False
        # Asignación de instancia propietaria
        self._ddl = instance
        # Asignación de instancia principal
        self._main = instance._main
        # Asignación del motor de conexión
        self._engine = instance._main._engine
        # Asignación de modelos iniciales
        self._base_models = list(initial_data.keys()) + [MODEL_NAME.BASE_USERS]

    def initialize_from_data(
        self,
    ) -> None:

        # Se realiza un intento por leer datos en la base de datos
        try:
            self._main.search(MODEL_NAME.BASE_MODEL)
            # Si existen datos se construye la estructura de modelos a partir de los datos
            self._build_instance_structure()
        # Si no existen los datos se realiza una inicialización desde cero
        except ProgrammingError as _:
            self._initialize()

        # Inicialización de atributos de los campos de los modelos
        self._main._strc.initialize_fields_atts()

    def _build_instance_structure(
        self,
    ) -> None:

        # Inicialización de modelos
        self._build_models_structure()

        # Inicialización de campos
        self._build_fields_structure()

    def _build_models_structure(
        self,
    ) -> None:

        # Lectura de todos los registros de modelos existentes
        model_records = self._main.search_read(
            MODEL_NAME.BASE_MODEL,
            [('model', 'not in', self._base_models)],
            ['name'],
            output_format= 'dict'
        )

        # Creación de los modelos de SQLAlchemy en la instancia
        for record in model_records:
            self._ddl._m_model.create_model(record['name'])

    def _build_fields_structure(
        self,
    ) -> None:
        
        # Lectura de todos los registros de campos existentes
        field_records = self._main.search_read(
            MODEL_NAME.BASE_MODEL_FIELD,
            ['&', ('id', '>', 40), ('name', 'not in', ['id', 'name', 'create_date', 'write_date'])],
            [
                'name',
                'model_id',
                'label',
                'ttype',
                'nullable',
                'is_required',
                'unique',
                'help_info',
                'related_model_id',
                'default_value',
            ],
            output_format= 'dict',
            only_ids_in_relations= True,
        )

        # Creación de las instancias de columna en los modelos de SQLAlchemy de la instancia
        for record in field_records:
            # Obtención del nombre del modelo al que el campo pertenece
            model_name = self._main.get_value(MODEL_NAME.BASE_MODEL, record['model_id'], 'model')
            # Obtención del modelo SQLAlchemy de la instancia
            model_model = self._main._models.get_table_model(model_name)
            # Creación del objeto de atributos de campo
            field_atts = self._ddl._m_model.build_field_atts(record)
            # Adición del campo al modelo SQLAlchemy
            self._ddl._m_model.add_field_to_model(model_model, field_atts)

        # Se establece el estado de inicialización a verdadero
        self._state = True

    def _initialize(
        self
    ) -> None:
        """
        ### Inicialización de base de datos
        Este método está diseñado para ser ejecutado una única vez en todo el ciclo de
        vida de la base de datos. Permite inicializar la estructura inicial de la base
        de datos para comenzar a trabajar con ella. Este método arrojará error tras 
        intentar ser ejecutado si existen datos en la base de datos.
        """

        # Si la base de datos ya está inicializada se aborta la operación
        if self._state:
            raise InitializationError(MESSAGES.RESET.ALREADY_INITIALIZED)

        # Inicialización de la base de datos
        self._main._base.metadata.create_all(self._engine)

        # Registro del usuario inicial
        self._main.create(MODEL_NAME.BASE_USERS, base_user)

        # Registro de los datos iniciales
        for ( model_name, data ) in initial_data.items():
            self._main.create(model_name, data)

        # Se añaden los campos 'create_uid' y'write_uid'
        self._add_uid_columns()

        # Se escribe usuario de creación y modificación en todos los registros existentes
        for model_name in self._base_models:
            self._main.update_where(model_name, [], {'create_uid': 1, 'write_uid': 1})

        # Se cambia el estado de inicialización a verdadero
        self._state = True

    def _drop_all(
        self
    ):
        """
        ### Eliminación de la base de datos
        ⚠️ Este método elimina todos los datos y tablas de la base de datos.
        """

        # Eliminación de todos los datos
        self._main._base.metadata.drop_all(self._engine)

        # Se reinicia el estado de inicialización
        self._state = False

    def _add_uid_columns(
        self
    ) -> None:
        """
        ### Creación de columnas de registro uid
        Este método interno ejecuta la creación de las columnas `create_uid` y
        `write_uid` en cada uno de los modelos registrados inicialmente en la base de
        datos.
        """

        # Obtención de las IDs de los modelos iniciales que existen registrados en la base de datos
        model_ids = self._main.search(MODEL_NAME.BASE_MODEL)

        # Creación de las columnas por cada modelo
        for model_id in model_ids:
            self._ddl.add_default_to_model(model_id)
