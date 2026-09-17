from typing import Callable
from typing import Generic
from typing import TYPE_CHECKING
from sqlalchemy.engine import Connection
from .._contexts.engines import BaseContext
from .._resources import DatabaseMetadata
from .._resources import ModelDataIndex
from .._resources import ModelsBearer
from .._resources import UserEnv
from .._typing.callables import NotifierInitializator
from .._typing.generics import MaybeNone
from .._typing.structures import NotificationTarget
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._engines import ActionEngine
    from .._engines import AutomationsEngine
    from .._engines import ComputeEngine
    from .._engines import PoliciesEngine
    from .._engines import ServerTasksEngine
    from .._engines import ValidationEngine
    from .._orchestrator import CRUD

class ExecutionContext(Generic[_M], BaseContext[_M]):
    """
    ## Contexto de ejecución
    La clase de contexto de ejecución es la usada en todas las transacciones CRUD
    expuestas en la instancia principal y hereda todas las propiedades de la clase
    `BaseContext`.

    ### ID del usuario que ejecuta la transacción
    Este es un atributo de solo lectura. Muestra la ID del usuario que está
    ejecutando la transacción.

    >>> ctx.uid
    >>> # [int]

    ### Creación de uno o muchos registros
    Este método realiza la creación de uno o muchos registros.

    Uso:
    >>> # Para un solo registro
    >>> record = {
    >>>     'login': 'onnymm',
    >>>     'name': 'Onnymm Azzur',
    >>> }
    >>> 
    >>> ctx.create('base.users', record)
    >>> 
    >>> # Para muchos registros
    >>> records = [
    >>>     {
    >>>         'login': 'onnymm',
    >>>         'name': 'Onnymm Azzur',
    >>>     },
    >>>     {
    >>>         'login': 'lumii',
    >>>         'name': 'Lumii Mynx',
    >>>     },
    >>> ]
    >>> 
    >>> ctx.create('base.users', records)

    ### Búsqueda de registros
    Este método retorna todas las IDs de los registros de un modelo o los registros
    que cumplan con la condición de búsqueda provista.

    Uso:
    >>> # Registros existentes en el modelo base.users
    >>> ctx.search('base.users')
    >>> # [1, 2, 3, 4, 5, 6, 7]
    >>> 
    >>> # Registros en el modelo base.users que hayan sido creados
    >>> #   por el usuario con la ID 2
    >>> ctx.search('base.users', [('create_uid', '=', 2)])
    >>> # [3, 5, 6]

    ### Lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros
    de un modelo de la base de datos a partir de una lista de IDs, en el orden en
    el que se especificaron los campos o todos los campos en caso de no haber sido
    especificados.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.read('base.users', [2])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 2
    >>> ctx.read('base.users', [2, 3])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> # ]
    >>> 
    >>> # Ejemplo 3
    >>> ctx.read('base.users', [2, 3], ['login', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> # ]

    ### Búsqueda y lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros
    de un modelo de la base de datos, en el orden en el que se especificaron los
    campos o todos los campos en caso de no haber sido especificados.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Ejemplo 2
    >>> ctx.search_read('base.users', [('user', '=', 'onnymm')])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 3
    >>> ctx.search_read('base.users', fields= ['user', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> #   ...
    >>> # ]

    ### Conteo de búsqueda
    Este método retorna el conteo de de todos los registros de un modelo o los
    registros que cumplan con la condición de búsqueda provista, ideal para
    funcionalidades de paginación que muestran un total de registros.

    Uso:
    >>> # Ejemplo 1
    >>> ctx.search_count('base.users')
    >>> # 5
    >>> 
    >>> # Ejemplo 2
    >>> ctx.search_count('base.permissions', [('create_uid', '=', 5)])
    >>> # 126

    ### Actualización de registros
    Este método realiza la actualización de uno o más registros a partir de su
    respectiva ID provista, actualizando uno o más campos con el valor provisto.
    Este método solo sobreescribe un mismo valor por cada campo a todos los
    registros provistos.

    Uso:
    >>> ctx.search_read('base.users', fields= ['login', 'name'])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii'},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim'},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio'},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Modificación
    >>> ctx.update('base.users', [3, 4, 5], {'name': 'Cambiado'})
    >>> # True
    >>> 
    >>> ctx.search_read('base.users', fields= ['login', 'name'])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
    >>> #   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
    >>> #   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
    >>> #   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
    >>> #   ...
    >>> # ]

    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Eliminación del registro con ID 2
    >>> 
    >>> ctx.delete('base.users', 2)
    >>> # True
    >>> 
    >>> ctx.search_read('base.users')
    >>> # [
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
    >>> #   ...
    >>> # ]

    ### Obtención de ID de recurso
    Este método se usa para obtener la ID de un registro en la base de datos
    señalado por su referencia única de mapeo.

    >>> ctx.get_resource_id('base_users.root_user')
    >>> # 1

    ### Ejecución de una acción
    Este método ejecuta una acción sobre un registro de un modelo en la base de
    datos. Para más información véase la sección [Acciones](#acciones).

    Ejemplo:
    >>> ctx.action('base.users', 'archive', 3)
    >>> # True

    En el fragmento de código ejecutamos una acción que archiva al registro con ID
    `3` del modelo `base.users`.
    """
    _to_execute_after_commit: list[Callable[[ExecutionContext[_M]], None]]

    def __init__(
        self,
        crud: CRUD,
        uid: int | str,
        conn: Connection,
        models_bearer: ModelsBearer[_M],
        database_metadata: DatabaseMetadata[_M],
        compute: 'ComputeEngine[_M]',
        automations: 'AutomationsEngine[_M]',
        validations: 'ValidationEngine[_M]',
        policies: 'PoliciesEngine[_M]',
        actions: 'ActionEngine[_M]',
        server_tasks: 'ServerTasksEngine[_M]',
        user_env_engine: UserEnv[_M],
        notifier_init: NotifierInitializator[_M],
    ) -> None:

        # Inicialización de entorno de usuario
        user_env = UserEnv(self, user_env_engine._resolvers)

        self._crud = crud
        self._model_data_index = ModelDataIndex(conn)
        self._uid = self.resolve_uid(uid)
        self.conn = conn
        self.models_bearer = models_bearer
        self.database_metadata = database_metadata
        self.compute = compute
        self.automations = automations
        self.validations = validations
        self.policies = policies
        self.actions = actions
        self.server_tasks = server_tasks
        self._execution_ctx = self
        self._env = user_env

        # Inicialización de lista de funciones a ejecutar después del commit
        self._to_execute_after_commit = []

        # Inicialización de notificador
        self._notifier = notifier_init(self)

    def get_resource_id(
        self,
        name: str,
    ) -> MaybeNone[int]:

        # Obtención de la ID de la referencia de recurso
        resource_id = self._model_data_index.get_resource_id(name)

        return resource_id

    def resolve_uid(
        self,
        uid: int | str
    ) -> int | None:

        # Si la ID de usuario provista es una referencia de recurso...
        if isinstance(uid, str):
            # Obtención de la ID de usuario desde la referencia de recurso
            uid = self._model_data_index.get_resource_id(uid)

            return uid
        # Si la ID de usuario provista es un entero...
        else:
            # Se usa ésta como valor de ID de usuario
            return uid

    def run_after_commit(
        self,
        fn: Callable[[ExecutionContext[_M]], None],
    ) -> None:

        # Se añade la función para ejecutarse tras el commit
        self._to_execute_after_commit.append(fn)

    def commit(
        self,
    ) -> None:
        """
        ### Commit
        Este método realiza un commit en la base de datos usando el método `commit` de
        la clase `Connection` de SQLAlchemy.

        **Parámetros**

        *No se requieren parámetros de entrada.*

        **Retorna**

        *Este método no retorna ningún valor.*
        """

        # Se realiza commit en la base de datos
        self.conn.commit()

        # Iteración por cada función a ejecutar
        for fn in self._to_execute_after_commit:
            # Se intenta ejecutar la función
            try:
                # Ejecución
                fn(self)
            # Si la ejecución falla...
            except Exception as e:
                # Notificación del error
                print(e)

        # Se eliminan las funciones suscritas
        self._to_execute_after_commit.clear()
        # Envío de notificaciones registradas
        self._notifier.flush()

    def _notify(
        self,
        event: str,
        target: NotificationTarget,
        payload: dict[str] = {},
        after_commit: bool = True,
    ) -> None:

        # Emisión de notificación
        self._notifier.notify(event, target, payload, after_commit)
