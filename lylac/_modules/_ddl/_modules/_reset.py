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
        self._base_models = list(initial_data.keys())

    def initialize(self) -> None:
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
        for ( table_name, data ) in initial_data.items():
            self._main.create(table_name, data)

        # Se añaden los campos 'create_uid' y'write_uid'
        self._add_uid_columns()

        # Se escribe usuario de creación y modificación en todos los registros existentes
        for model_name in self._base_models + [MODEL_NAME.BASE_USERS]:
            self._main.update_where(model_name, [], {'create_uid': 1, 'write_uid': 1})

        # Se cambia el estado de inicialización a verdadero
        self._state = True

    def _drop_all(self):
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
