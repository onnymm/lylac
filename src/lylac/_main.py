from typing import Callable
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Union
from sqlalchemy.engine import Connection
from sqlalchemy.exc import ProgrammingError
from ._api import _MainAPI
from ._constants import MODEL_NAME
from ._constants import MONITOR
from ._constants import INITIAL_PACKAGES
from ._constants import REF
from ._contexts import ActionContext as _ActionContext
from ._contexts import AutomationContext as _AutomationContext
from ._contexts import ComputeContext as _ComputeContext
from ._contexts import ExecutionContext as _ExecutionContext
from ._contexts import ServerTaskContext as _ServerTaskContext
from ._contexts import TransactionContext as _TransactionContext
from ._contexts import ValidationContext as _ValidationContext
from ._contexts import ValueResolutionContext as _ValueResolutionContext
from ._core.models import _Base
from ._data import build_database_structure
from ._data import build_initial_data
from ._engines import ActionEngine
from ._engines import AutomationsEngine
from ._engines import ComputeEngine
from ._engines import PoliciesEngine
from ._engines import ServerTasksEngine
from ._engines import UserEnvEngine
from ._engines import ValidationEngine
from ._integrations import ModulesManager
from ._operations import DDL
from ._orchestrator import CRUD
from ._resources import DatabaseMetadata
from ._resources import ModelsBearer
from ._services import DefaultNotifier
from ._services import EngineService
from ._typing.aliases import FieldName
from ._typing.callables import ExecutableTransactionCallback
from ._typing.callables import ComputeFieldFn as _ComputeFieldFn
from ._typing.callables import NotifierInitializator
from ._typing.generics import ScalarOrIterable
from ._typing.generics import ModelName
from ._typing.generics import _Record
from ._typing.structures import CriteriaStructure
from ._typing.structures import InputRecordData
from ._typing.structures import FieldReadDeclaration
from ._typing.type_parameters import _M
from ._typing.type_parameters import _R
from ._typing.type_parameters import _T
from .security import build_authenticate_user_callback
from .security import build_login_callback

class Lylac(Generic[_M]):
    """
    # Lylac
    Un framework ORM programable para PostgreSQL, diseñado para plataformas
    empresariales extensibles.

    ## Inicialización

    ### Variables de entorno
    Para inicializar la estructura inicial de una base de datos se requieren configurar
    las siguientes variables de entorno:

    #### Credenciales
    Las siguientes variables pertenecen a las credenciales necesarias para conectarse a
    la base de datos.

    | Variable         | Descripción                          |
    |------------------|--------------------------------------|
    | `LYLAC_HOST`     | URL donde se aloja la base de datos. |
    | `LYLAC_PORT`     | Puerto.                              |
    | `LYLAC_NAME`     | Nombre de la base de datos.          |
    | `LYLAC_USER`     | Nombre de usuario administrador.     |
    | `LYLAC_PASSWORD` | Contraseña de acceso.                |

    Ejemplo:
    ```
    LYLAC_HOST = https://wwww.mydatabasehost.com
    LYLAC_PORT = 5432
    LYLAC_NAME = production
    LYLAC_USER = admin
    LYLAC_PASSWORD = mypassword123
    ```

    #### Usuarios
    Se requiere configurar dos usuarios iniciales a la base de datos. Un usuario raíz
    que se usará como autor de la creación de los registros de la estructura base de la
    base de datos y un usuario administrador. Puede ser tu usuario.

    | Variable                 | Descripción                                    |
    |--------------------------|------------------------------------------------|
    | `LYLAC_ROOT_USER_NAME`   | Nombre del usuario raíz.                       |
    | `LYLAC_ROOT_USER_LOGIN`  | Nombre de usuario de acceso del usuario raíz.  |
    | `LYLAC_ADMIN_USER_NAME`  | Nombre del usuario administrador.              |
    | `LYLAC_ADMIN_USER_LOGIN` | Nombre de usuario de acceso del administrador. |

    Ejemplo:
    ```
    LYLAC_ROOT_USER_NAME = Root
    LYLAC_ROOT_USER_LOGIN = lylac_root
    LYLAC_ADMIN_USER_NAME = "Onnymm Azzur"
    LYLAC_ADMIN_USER_LOGIN = onnymm
    ```

    > `i` El usuario raíz aparecerá archivado una vez que se inicialice la base de
    datos.

    #### Parámetros opcionales
    También se pueden configurar algunos parámetros opcionales para personalizar más el
    flujo de trabajo del framework.

    | Variable                 | Descripción                                                                  |
    |--------------------------|------------------------------------------------------------------------------|
    | `LYLAC_DEFAULT_PASSWORD` | Contraseña predeterminada que se le asigna a un usuario cuando se crea éste. |

    ### Creación de la base de datos
    Se puede comenzar con un archivo muy pequeño como el siguiente.

    >>> from lylac import Lylac
    >>> 
    >>> db = Lylac()

    Al ejecutar el archivo por primera vez, se imprimirá la siguiente leyenda en
    consola:

    `La base de datos de inicializó correctamente.`

    ## Iniciar sesión
    Este método permite crear una sesión de usuario y retorna una UUID de sesión para
    poder autenticarse cuando se use alguno de los métodos de transacción de datos.

    Uso:
    >>> # Obtención de UUID de sesión de autenticación
    >>> session_uuid = db.login('onnymm', 'contraseñasecreta123')

    ## Creación de uno o muchos registros
    Este método realiza la creación de uno o muchos registros.

    Uso:
    >>> # Para un solo registro
    >>> record = {
    >>>     'login': 'onnymm',
    >>>     'name': 'Onnymm Azzur',
    >>> }
    >>> 
    >>> db.create(session_uuid, 'base.users', record)
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
    >>> db.create(session_uuid, 'base.users', records)

    ## Búsqueda de registros
    Este método retorna todas las IDs de los registros de un modelo o los registros que
    cumplan con la condición de búsqueda provista.

    Uso:
    >>> # Registros existentes en el modelo base.users
    >>> db.search(session_uuid, 'base.users')
    >>> # [1, 2, 3, 4, 5, 6, 7]
    >>> 
    >>> # Registros en el modelo base.users que hayan sido creados
    >>> #   por el usuario con la ID 2
    >>> db.search(session_uuid, 'base.users', [('create_uid', '=', 2)])
    >>> # [3, 5, 6]

    ## Lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros de
    un modelo de la base de datos a partir de un iterable de IDs, en el orden en el que
    se especificaron los campos o todos los campos en caso de no haber sido
    especificados.

    Uso:
    >>> # Ejemplo 1
    >>> db.read(session_uuid, 'base.users', [2])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 2
    >>> db.read(session_uuid, 'base.users', [2, 3])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> # ]
    >>> 
    >>> # Ejemplo 3
    >>> db.read(session_uuid, 'base.users', [2, 3], ['login', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> # ]

    ## Búsqueda y lectura de registros
    Este método retorna una lista de diccionarios con el contenido de los registros de
    un modelo de la base de datos, en el orden en el que se especificaron los campos o
    todos los campos en caso de no haber sido especificados.

    Uso:
    >>> # Ejemplo 1
    >>> db.search_read(session_uuid, 'base.users')
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   ...
    >>> # ]
    >>> 
    >>> # Ejemplo 2
    >>> db.search_read(session_uuid, 'base.users', [('user', '=', 'onnymm')])
    >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
    >>> 
    >>> # Ejemplo 3
    >>> db.search_read(session_uuid, 'base.users', fields= ['user', 'create_date'])
    >>> # [
    >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
    >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
    >>> #   ...
    >>> # ]

    ## Conteo de búsqueda
    Este método retorna el conteo de de todos los registros de un modelo o los
    registros que cumplan con la condición de búsqueda provista, ideal para
    funcionalidades de paginación que muestran un total de registros.

    Uso:
    >>> # Ejemplo 1
    >>> db.search_count(session_uuid, 'base.users')
    >>> # 5
    >>> 
    >>> # Ejemplo 2
    >>> db.search_count(session_uuid, 'base.permissions', [('create_uid', '=', 5)])
    >>> # 126

    ## Actualización de registros
    Este método realiza la actualización de uno o más registros a partir de su
    respectiva ID provista, actualizando uno o más campos con el valor provisto. Este
    método solo sobreescribe un mismo valor por cada campo a todos los registros
    provistos.

    Uso:
    >>> db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
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
    >>> db.update(session_uuid, 'base.users', [3, 4, 5], {'name': 'Cambiado'})
    >>> # True
    >>> 
    >>> db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
    >>> # [
    >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
    >>> #   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
    >>> #   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
    >>> #   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
    >>> #   ...
    >>> # ]

    ## Eliminación de registros
    Este método realiza la eliminaciónd e uno o más registros de la base de datos a
    partir de su respectiva ID provista.

    Uso:
    >>> db.search_read(session_uuid, 'base.users')
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
    >>> db.delete(session_uuid, 'base.users', 2)
    >>> # True
    >>> 
    >>> db.search_read(session_uuid, 'base.users')
    >>> # [
    >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
    >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
    >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
    >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
    >>> #   ...
    >>> # ]

    ## Autenticación de usuario
    Este método recibe una UUID de sesión y resuelve a qué usuario le pertenece la
    sesión.

    Uso:
    >>> session_uuid = '4d9ad73f-40cf-4b33-8feb-4c593c172cf2'
    >>> 
    >>> db.authenticate_user(session_uuid)
    >>> # 2
    """
    # Interfaz para acceso al tipado de automatización sin tener que colocar literal de modelos
    type ActionContext[T] = _ActionContext[_M, Union[T, _R]]
    type AutomationContext[T] = _AutomationContext[_M, T]
    type ValidationContext[T] = _ValidationContext[_M, T]
    type ValueResolutionContext[T] = _ValueResolutionContext[_M, Union[T, _R]]
    type ServerTaskContext = _ServerTaskContext[_M]
    type TransactionContext = _TransactionContext[ModelName[_M]]
    type ExecutionContext = _ExecutionContext[_M]
    type ComputeContext = _ComputeContext[_M]
    type ComputeFieldFn = _ComputeFieldFn[_M]
    # Atributos
    api: _MainAPI[_M]
    _crud: CRUD[_M]
    _metadata: DatabaseMetadata
    _models_bearer: ModelsBearer[_M]
    _ddl: DDL[_M]
    _engine: EngineService
    _is_first_initialization: bool
    _populate_models_fn: ExecutableTransactionCallback[_M]

    def __init__(
        self,
        build_models_fn: ExecutableTransactionCallback[_M] = lambda _: None,
        populate_models_fn: ExecutableTransactionCallback[_M] = lambda _: None,
        notifier_init: NotifierInitializator[_M] = lambda ctx: DefaultNotifier(ctx.uid),
    ) -> None:

        # Asignación de valores
        self._populate_models_fn = populate_models_fn
        self._notifier_init = notifier_init

        # Inicialización de instancia de servicio de conexión a la base de datos
        self._engine = EngineService()
        # inicialización de instancia de portador de modelos
        self._models_bearer = ModelsBearer[_M]()
        # Inicialización de instancia de metadatos de la base de datos
        self._metadata = DatabaseMetadata[_M]()
        # Inicialización de orquestador CRUD
        self._crud = CRUD[_M](self._models_bearer)
        # Inicialización de instancia de operaciones DDL
        self._ddl = DDL[_M](self._models_bearer, self._metadata)
        # Inicialización de extensión de módulos
        self.modules = ModulesManager[_M](self)

        # Se intenta inicializar la instancia con datos existentes
        try:
            # Inicialización desde datos existentes de la base de datos
            self._load_from_built_database()

        except ProgrammingError:
            # Se construye la estructura de la base de datos
            self._build_database_structure(build_models_fn)

    def populate_if_first_initialization(
        self,
    ) -> None:

        # Si es la primera inicialización en base de datos...
        if self._is_first_initialization:
            # Ejecución de la función provista para poblar los modelos
            self._execute_as_root(self._populate_models_fn)

        # Se establece el bypass en Falso
        self._crud.PERMISSIONS_BYPASS = False

    def login(
        self,
        username: str,
        password: str,
    ) -> str:
        """
        ## Iniciar sesión
        Este método permite crear una sesión de usuario y retorna una UUID de sesión
        para poder autenticarse cuando se use alguno de los métodos de transacción de
        datos.

        Uso:
        >>> # Obtención de UUID de sesión de autenticación
        >>> session_uuid = db.login('onnymm', 'contraseñasecreta123')

        **Parámetros**
        :username: Nombre de usuario.
        :password: Contraseña del usuario.

        **Retorno**
        :session_uuid: UUID de sesión para autenticación del usuario.

        ### Errores comunes
        - `UserNotFoundError`: El usuario no fue encontrado.
        - `UserNotActiveError`: El usuario fue encontrado pero éste no está activo.
        - `IncorrectPasswordError`: El usuario fue encontrado y está activo pero la
        contraseña no coincide con la almacenada en la base de datos.

        > `i` Es decisión del desarrollador proveer o no la información sobre la falla
        encontrada en el inicio de sesión, por ejemplo, si desea decirle al usuario
        que su cuenta no existe o solo hacerle saber que "El usuario o la contraseña
        no son correctos".
        """

        # Construcción de la transacción de inicio de sesión
        transaction = build_login_callback(self, username, password)

        # Ejecución de la función de transacción
        session_uuid = self._engine.execute_complex(transaction)

        return session_uuid

    def execute_transaction(
        self,
        session_uuid: str,
        callback: Callable[[_ExecutionContext[_M]], _T],
    ) -> _T:
        """
        ## Ejecutar transacción
        Este método ejecuta una transacción compleja construida mediante una función
        que es provista a este método como argumento. La función debe estar preparada
        para recibir como argumento un `ExecutionContext[_M]` para poder declarar
        instrucciones de operaciones en la base de datos. Al estar asociadas a una
        misma transacción, las instrucciones pueden confirmarse o revertirse como una
        sola unidad. Si ocurre un error durante la ejecución, la transacción puede
        realizar un rollback, evitando que los cambios realizados hasta ese momento
        sean persistidos parcialmente en la base de datos.

        Uso:
        >>> # Definición de función de lectura del perfil del usuario de la sesión
        >>> def me(ctx: Lylac.ExecutionContext):
        >>> 
        >>>     # Obtención de los datos del usuario de la sesión
        >>>     [ user_data ] = ctx.read(
        >>>         'base.users',
        >>>         ctx.uid,
        >>>         fields = [
        >>>             'name',
        >>>             'active',
        >>>             'login',
        >>>             'profile_picture',
        >>>         ],
        >>>     )
        >>> 
        >>>     return user_data
        >>> 
        >>> # Ejecución de la transacción desde la instancia principal
        >>> profile_data = db.execute_transaction(session_uuid, me)

        **Parámetros**

        :session_uuid: UUID de sesión.
        :callback: Función de transacción.

        **Retorno**

        :result: El valor u objeto que retorna la función de transacción.
        """

        # Autenticación del usuario
        uid = self.authenticate_user(session_uuid)

        def wrapped_transaction(conn: Connection) -> _T:
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(uid, conn)
            # Ejecución de la función
            closure_result = callback(execution_ctx)

            # Se realiza commit
            execution_ctx.commit()

            return closure_result

        # Ejecución de la función de transacción
        result = self._engine.execute_complex(wrapped_transaction)

        return result

    def action(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        name: str,
        record_id: int,
    ) -> Literal[True]:
        """
        ## Ejecución de una acción
        Este método ejecuta una acción sobre un registro de un modelo en la base de
        datos.

        Ejemplo:
        >>> db.action(session_uuid, 'base.users', 'archive', 3)
        >>> # True

        En el fragmento de código ejecutamos una acción que archiva al registro con ID
        `3` del modelo `base.users`.

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :name: Nombre de la acción.
        :record_id: ID del registro sobre el que se va a ejecutar la acción.

        **Retorno**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> Literal[True]:
            # Ejecución de la acción
            closure_result = self._actions.execute(
                execution_ctx,
                model_name,
                name,
                record_id,
            )

            return closure_result

        # Ejecución de la transacción
        result = self.execute_transaction(session_uuid, transaction)

        return result

    def task(
        self,
        session_uuid: str,
        name: str,
    ) -> Literal[True]:
        """
        ## Ejecución de tarea de servidor
        Este método ejecuta una tarea de servidor en la base de datos.

        Ejemplo:
        >>> db.task(session_uuid, 'update_data_from_api')
        >>> # True

        **Parámetros**

        :session_uuid: UUID de sesión.
        :name: Nombre de la tarea de servidor.

        **Retorno**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> Literal[True]:
            # Ejecución de la tarea de servidor
            closure_result = self._server_tasks.execute(execution_ctx, name)

            return closure_result

        # Ejecución de la transacción
        result = self.execute_transaction(session_uuid, transaction)

        return result

    def create(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        data: ScalarOrIterable[InputRecordData[_M]],
    ) -> list[int]:
        """
        ## Creación de uno o muchos registros
        Este método realiza la creación de uno o muchos registros.

        Uso:
        >>> # Para un solo registro
        >>> record = {
        >>>     'login': 'onnymm',
        >>>     'name': 'Onnymm Azzur',
        >>> }
        >>> 
        >>> db.create(session_uuid, 'base.users', record)
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
        >>> db.create(session_uuid, 'base.users', records)
        >>> 
        >>> # Podemos crear o añadir registros referenciados directamente
        >>> #    con un comando de relación
        >>> db.create(
        >>>     session_uuid,
        >>>     'base.users',
        >>>     {
        >>>         'login': 'onnymm',
        >>>         'name': 'Onnymm Azzur',
        >>>         # Campo de tipo [many2many]
        >>>         'role_ids': {
        >>>             # Comando de relación de creación
        >>>             'create': {
        >>>                 'name': 'command_admin',
        >>>                 'label': 'Administrador de comandos',
        >>>                 ...
        >>>             },
        >>>             # Comando de relación de adición
        >>>             'add': {
        >>>                 'add': [1, 2, 3] # Registros que ya existen
        >>>             },
        >>>         },
        >>>     },
        >>> )

        Se pueden proporcionar también funciones de resolución de valor:
        >>> db.create(
        >>>     session_uuid,
        >>>     'base.model.field',
        >>>     {
        >>>         'name': 'hire_date',
        >>>         'label': 'Fecha de contrato',
        >>>         'ttype': 'date',
        >>>         # Función de resolución para asignar una ID
        >>>         'model_id': lambda ctx: ctx.get_resource_id('base_model.hr_employee'),
        >>>     },
        >>> )

        Antes de que el registro sea ingresado para ser creado en la base de datos, la
        función de resolución de valor es ejecutada usando un contexto de resolución de
        valor. La ID del modelo se obtiene, se reemplaza la función por el valor y
        entonces el registro es enviado para ser creado:
        >>> {
        >>>     'name': 'hire_date',
        >>>     'label': 'Fecha de contrato',
        >>>     'ttype': 'date',
        >>>     'model_id': 27,
        >>> }

        `i` Para este caso también podríamos modificar directamente el registro del
        modelo `hr.employee` (Si contamos con la ID) y modificar el campo de
        `field_ids` usando un *Comando de Relación* de creación proporcionando los
        datos del campo a crear.

        Los valores para cada valor pueden ser cualquiera de:
        - `DMLScalarCompatible` — Tipo de dato que se puede usar como valor para un
        campo de modelo. El tipo de dato puede ser:
            - `int`
            - `float`
            - `str`
            - `bool`
            - `datetime.date`
            - `datetime.datetime`
            - `datetime.time`
            - `datetime.timedelta`
            - `None`
        - `JSONLike` — Estructura equivalente a JSON. El tipo de dato puede ser escalar
        o iterable de:
            - `JSONLikeScalar` — Representa los tipos:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `None`
            - `JSONLikeObjShape` — Representa un diccionario serializable conformado
        por:
                - Llaves que deben ser de tipo `str`
                - Valores que pueden ser escalar o iterable de:
                    - `JSONLikeScalar`
                    - `JSONLike`
        - `InputRecordData` — Datos para crear un registro vinculado, en campos de tipo
        `many2one`.
        - `RelationCommands` — Comandos de modificación de los registros referenciados
        en campos de tipo `one2many` y `many2many` desde el registro que los
        referencía. Las llaves y valores del diccionario pueden ser:
            - `'create'` — Comando de relación de creación.
            - `'add'` — Comando de relación de adición.
            - `'update'` — Comando de relación de actualización.
            - `'replace'` — Comando de relación de reemplazo.
            - `'unlink'` — Comando de relación de desvinculación.
            - `'delete'` — Comando de relación de eliminación.
            - `'clear'` — Comando de relación de limpieza.
        - `ValueResolutionFn` — Función de resolución de valor que se usa para resolver
        y retornar un valor que se usará en el campo para almacenarse en la base de
        datos.

        **Parámetros**

        :session_uuid:  UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :data: Diccionario o iterable de diccionarios de los datos a crear.

        **Retorna**

        :record_ids: Lista de IDs del registro o de los registros creados.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> list[int]:
            # Creación de registros y obtención de las IDs creadas
            closure_created_ids = self._crud.create(execution_ctx, model_name, data)
            # Se realiza commit
            execution_ctx.commit()

            return closure_created_ids

        # Ejecución de la transacción
        created_ids = self.execute_transaction(session_uuid, transaction)

        return created_ids

    def search(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure[_M] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:
        """
        ## Búsqueda de registros
        Este método retorna todas las IDs de los registros de un modelo o los registros
        que cumplan con la condición de búsqueda provista.

        Uso:
        >>> # Registros existentes en el modelo base.users
        >>> db.search(session_uuid, 'base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]
        >>> 
        >>> # Registros en el modelo base.users que hayan sido creados
        >>> #   por el usuario con la ID 2
        >>> db.search(session_uuid, 'base.users', [('create_uid', '=', 2)])
        >>> # [3, 5, 6]

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> db.search(
        >>>     session_uuid,
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # [5]

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> db.search(
        >>>     session_uuid,
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # [3, 4, 5, 6, 7, ...]

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total

        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)

        >>> db.search(
        >>>     session_uuid,
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # [24, 31, 56, 89, ...]

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
        Este tipo de dato representa una condición para usarse en una transacción en
        base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Referencia de campo. Puede ser alguno de los siguientes tipos:
            - `FieldName`: Nombre del campo del modelo o referencia *Many2One*
            - `FieldComputation`: Cómputo de campo.
        Nombre del campo del modelo, referencia many2one o campo computado
        2. Operador de comparación. Puede ser alguno de los siguientes literales:
            - `'='`: Igual a
            - `'!='`: Diferente de
            - `'=?'`: No está establecido o es igual a
            - `'>'`: Mayor a
            - `'>='`: Mayor o igual a
            - `'<'`: Menor que
            - `'<='`: Menor o igual que
            - `'in'`: Está en
            - `'not in'`: No está en
            - `'like'`: Contiene (sensible a mayúsculas y minúsculas)
            - `'ilike'`: Contiene (no sensible a mayúsculas y minúsculas)
            - `'not like'`: No contiene (sensible a mayúsculas y minúsculas)
            - `'not ilike'`: No contiene (no sensible a mayúsculas y minúsculas)
            - `'starts with'`: Comienza con (sensible a mayúsculas y minúsculas)
            - `'ends with'`: Termina con (sensible a mayúsculas y minúsculas)
            - `'~'`: Coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
            - `!'~'`: No coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
        3. Valor de comparación. Puede ser alguno de los siguientes tipos:
            - `ScalarOrIterable[DMLScalarCompatible]`Escalar o iterable de Tipo de dato
            que se puede usar como valor para un campo de modelo. El tipo de dato puede
            ser:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `datetime.date`
                - `datetime.datetime`
                - `datetime.time`
                - `datetime.timedelta`
                - `None`
            - `ValueResolutionFn[_M]`: Función de resolución de valor que se usa para
            resolver y retornar un valor que se usará en el campo para almacenarse en
            la base de datos

        Algunos ejemplos de tripletas:
        >>> ('name', 'like', 'Onnymm')
        >>> # El nombre contiene 'Onnymm'
        >>> ('id', '=', 5)
        >>> # La ID es igual a 5
        >>> ('create_uid.name', 'ends with', 'Azzur')
        >>> # El nombre del usuario creador del registro termina con "Azzur"
        >>> ('device_id.type_id.create_date', '=', lambda ctx: ctx.today())
        >>> # La fecha de creación del tipo de dispostivo del dispositivo es igual a hoy
        >>> (('subtotal', 'float', lambda ctx: ctx['qty'] * ctx['price']), '<', 500)
        >>> # El cómputo del subtotal es menor a 500

        Las tuplas de estructura se deben unir por medio de un operador lógico que va
        al principio. Por ejemplo:
        >>> ('amount', '>', 500)
        >>> # El monto es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # El nombre contiene "as"
        >>> 
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # El monto es mayor a 500 y el nombre contiene "as"
        ----

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado
        por éste. Suponiendo que una búsqueda normal arrojaría los siguientes
        resultados:
        >>> db.search(session_uuid, 'base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que el retorno de los registros considerará solo a partir
        desde cierto desfase numérico, como por ejemplo lo siguiente:
        >>> db.search(session_uuid, 'base.users', offset= 2)
        >>> # [3, 4, 5, 6, 7]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de
        datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
        >>> db.search(session_uuid, 'base.users')
        >>> # [1, 2, 3, 4, 5, 6, 7]

        Se puede especificar que solo se requiere obtener una cantidad máxima de
        registros a partir de un número provisto:
        >>> db.search(session_uuid, 'base.users', limit= 3)
        >>> # [1, 2, 3]

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.
        :offset: Desfase de resultados retornados.
        :limit: Límite de cantidad de resultados retornados.

        **Retorna**

        :record_ids: Lista de IDs del registro o de los registros creados.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> list[int]:
            # Obtención de los datos
            closure_found_ids = self._crud.search(
                execution_ctx,
                model_name,
                search_criteria,
                offset,
                limit,
            )

            return closure_found_ids

        # Ejecución de la transacción
        found_ids = self.execute_transaction(session_uuid, transaction)

        return found_ids

    def read(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        record_ids: ScalarOrIterable[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ScalarOrIterable[FieldName]] = None,
        ascending: Optional[ScalarOrIterable[bool]] = None,
    ) -> list[_Record]:
        """
        ## Lectura de registros
        Este método retorna una lista de diccionarios con el contenido de los registros
        de un modelo de la base de datos a partir de un iterable de IDs, en el orden en
        el que se especificaron los campos o todos los campos en caso de no haber sido
        especificados.

        Uso:
        >>> # Ejemplo 1
        >>> db.read(session_uuid, 'base.users', [2])
        >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
        >>> 
        >>> db.read(session_uuid, 'base.users', [2, 3])
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> # ]
        >>> 
        >>> # Especificación de campos a leer
        >>> db.read(session_uuid, 'base.users', [2, 3], ['login', 'create_date'])
        >>> # [
        >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
        >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
        >>> # ]
        >>> 
        >>> db.read(
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         # Campos existentes en la base de datos
        >>>         'name',
        >>>         'subtotal',
        >>>         'user_id',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id': [2, 'Onnymm Azzur']},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id': [2, 'Usuario Root']},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id': [3, 'Mynx Lumii']},
        >>> # ]

        Se puede acceder a los atributos de los registros referenciados:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cadena de referencias [many2one]
        >>>         'user_id.active',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id.active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id.active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id.active': True},
        >>> # ]

        Uso de campos con un alias:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo con alias
        >>>         ('user_id.active', 'is_user_active'),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'is_user_active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'is_user_active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'is_user_active': True},
        >>> # ]

        Uso de cómputo de campo:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [1, 2, 3],
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cómputo de campo
        >>>         ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'total': 272.77},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'total': 281.95},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'total': 1174.15},
        >>> # ]

        Con expansión de campos en campos de tipo `one2many` y `many2many`:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo [one2many]
        >>>         'line_ids',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [1, 2],
        >>> #     },
        >>> # ]
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 'product_id',
        >>>                 'quantity',
        >>>                 'subtotal',
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id': [13, 'Café sencillo'], 'quantity': 1, 'subtotal': 35.15},
        >>> #             {'id': 2, 'product_id': [2, 'Taza de café'], 'quantity': 1, 'subtotal': 200.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        Se pueden usar múltiples tipos de entrada:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 # Cadena de referencia
        >>>                 'product_id.code',
        >>>                 # Alias
        >>>                 ('quantity', 'qty'),
        >>>                 # Cómputo de campo
        >>>                 ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        Alias a la expansión de campos:
        >>> db.read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     1,
        >>>     [
        >>>         ...,
        >>>         (
        >>>             # Expansión de campos
        >>>             (
        >>>                 'line_ids',
        >>>                 [
        >>>                     'product_id.code',
        >>>                     ...,
        >>>                 ],
        >>>             ),
        >>>             # Asignación de alias
        >>>             'detail',
        >>>         )
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'detail': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> # ]

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o iterable de IDs de los registros a leer.
        :fields: Declaración de campos a leer.
        :sortby: Nombre o nombres de campo a usar para ordenar los registros.
        :ascending: Dirección de ordenamiento, ascendente (*True*) o descendente
        (*False*).

        **Retorna**

        :records: Lista de diccionarios con los datos de los registros solicitados.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> list[_Record]:
            # Obtención de los datos
            closure_data = self._crud.read(
                execution_ctx,
                model_name,
                record_ids,
                fields,
                sortby,
                ascending,
            )

            return closure_data

        # Ejecución de la transacción
        data = self.execute_transaction(session_uuid, transaction)

        return data

    def search_read(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure[_M] = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ScalarOrIterable[FieldName]] = None,
        ascending: Optional[ScalarOrIterable[bool]] = None,
    ) -> list[_Record]:
        """
        ## Búsqueda y lectura de registros
        Este método retorna una lista de diccionarios con el contenido de los registros
        de un modelo de la base de datos, en el orden en el que se especificaron los
        campos o todos los campos en caso de no haber sido especificados.

        Uso:
        >>> db.search_read(session_uuid, 'base.users')
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   ...
        >>> # ]
        >>> 
        >>> db.search_read(session_uuid, 'base.users', [('user', '=', 'onnymm')])
        >>> # [{'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...}]
        >>> 
        >>> # Especificación de campos
        >>> db.search_read(session_uuid, 'base.users', fields= ['user', 'create_date'])
        >>> # [
        >>> #   {'id': 2, 'login': 'onnymm', 'create_date': '2026-09-12 12:15:36' ...},
        >>> #   {'id': 3, 'login': 'lumii', 'create_date': '2026-09-12 13:28:14 ...},
        >>> #   ...
        >>> # ]

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # [...]

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # [...]

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total
        >>> 
        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)
        >>> 
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # [...]

        Para lectura de campos:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         # Campos existentes en la base de datos
        >>>         'name',
        >>>         'subtotal',
        >>>         'user_id',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id': [2, 'Onnymm Azzur']},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id': [2, 'Usuario Root']},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id': [3, 'Mynx Lumii']},
        >>> #     ...,
        >>> # ]

        Se puede acceder a los atributos de los registros referenciados:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cadena de referencias [many2one]
        >>>         'user_id.active',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'user_id.active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'user_id.active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'user_id.active': True},
        >>> #     ...
        >>> # ]

        Uso de campos con un alias:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo con alias
        >>>         ('user_id.active', 'is_user_active'),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'is_user_active': True},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'is_user_active': False},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'is_user_active': True},
        >>> #     ...,
        >>> # ]

        Uso de cómputo de campo:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Cómputo de campo
        >>>         ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {'id': 1, 'name': 'S00000', 'subtotal': 235.15, 'total': 272.77},
        >>> #     {'id': 2, 'name': 'S00001', 'subtotal': 587.89, 'total': 281.95},
        >>> #     {'id': 3, 'name': 'S00002', 'subtotal': 1012.20, 'total': 1174.15},
        >>> #     ...,
        >>> # ]

        Con expansión de campos en campos de tipo `one2many` y `many2many`:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         'name',
        >>>         'subtotal',
        >>>         # Campo [one2many]
        >>>         'line_ids',
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [1, 2],
        >>> #     },
        >>> #     ...,
        >>> # ]
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 'product_id',
        >>>                 'quantity',
        >>>                 'subtotal',
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id': [13, 'Café sencillo'], 'quantity': 1, 'subtotal': 35.15},
        >>> #             {'id': 2, 'product_id': [2, 'Taza de café'], 'quantity': 1, 'subtotal': 200.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        Se pueden usar múltiples tipos de entrada:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             'line_ids',
        >>>             # Campos de los registros de líneas
        >>>             [
        >>>                 # Cadena de referencia
        >>>                 'product_id.code',
        >>>                 # Alias
        >>>                 ('quantity', 'qty'),
        >>>                 # Cómputo de campo
        >>>                 ('total', 'float', lambda ctx: ctx['subtotal'] * 1.16),
        >>>             ],
        >>>         ),
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'line_ids': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        Alias a la expansión de campos:
        >>> db.search_read(
        >>>     session_uuid,
        >>>     'sale.order',
        >>>     [
        >>>         ...,
        >>>         (
        >>>             # Expansión de campos
        >>>             (
        >>>                 'line_ids',
        >>>                 [
        >>>                     'product_id.code',
        >>>                     ...,
        >>>                 ],
        >>>             ),
        >>>             # Asignación de alias
        >>>             'detail',
        >>>         )
        >>>     ]
        >>> )
        >>> # [
        >>> #     {
        >>> #         'id': 1,
        >>> #         'name': 'S00000',
        >>> #         'subtotal': 235.15,
        >>> #         'detail': [
        >>> #             {'id': 1, 'product_id.code': '00COFFEE', 'qty': 1, 'subtotal': 40.77},
        >>> #             {'id': 2, 'product_id.code': 'CUP-BK', 'qty': 1, 'subtotal': 232.00},
        >>> #         ],
        >>> #     },
        >>> #     ...,
        >>> # ]

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
        Este tipo de dato representa una condición para usarse en una transacción en
        base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Referencia de campo. Puede ser alguno de los siguientes tipos:
            - `FieldName`: Nombre del campo del modelo o referencia *Many2One*
            - `FieldComputation`: Cómputo de campo.
        Nombre del campo del modelo, referencia many2one o campo computado
        2. Operador de comparación. Puede ser alguno de los siguientes literales:
            - `'='`: Igual a
            - `'!='`: Diferente de
            - `'=?'`: No está establecido o es igual a
            - `'>'`: Mayor a
            - `'>='`: Mayor o igual a
            - `'<'`: Menor que
            - `'<='`: Menor o igual que
            - `'in'`: Está en
            - `'not in'`: No está en
            - `'like'`: Contiene (sensible a mayúsculas y minúsculas)
            - `'ilike'`: Contiene (no sensible a mayúsculas y minúsculas)
            - `'not like'`: No contiene (sensible a mayúsculas y minúsculas)
            - `'not ilike'`: No contiene (no sensible a mayúsculas y minúsculas)
            - `'starts with'`: Comienza con (sensible a mayúsculas y minúsculas)
            - `'ends with'`: Termina con (sensible a mayúsculas y minúsculas)
            - `'~'`: Coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
            - `!'~'`: No coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
        3. Valor de comparación. Puede ser alguno de los siguientes tipos:
            - `ScalarOrIterable[DMLScalarCompatible]`Escalar o iterable de Tipo de dato
            que se puede usar como valor para un campo de modelo. El tipo de dato puede
            ser:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `datetime.date`
                - `datetime.datetime`
                - `datetime.time`
                - `datetime.timedelta`
                - `None`
            - `ValueResolutionFn[_M]`: Función de resolución de valor que se usa para
            resolver y retornar un valor que se usará en el campo para almacenarse en
            la base de datos

        Algunos ejemplos de tripletas:
        >>> ('name', 'like', 'Onnymm')
        >>> # El nombre contiene 'Onnymm'
        >>> ('id', '=', 5)
        >>> # La ID es igual a 5
        >>> ('create_uid.name', 'ends with', 'Azzur')
        >>> # El nombre del usuario creador del registro termina con "Azzur"
        >>> ('device_id.type_id.create_date', '=', lambda ctx: ctx.today())
        >>> # La fecha de creación del tipo de dispostivo del dispositivo es igual a hoy
        >>> (('subtotal', 'float', lambda ctx: ctx['qty'] * ctx['price']), '<', 500)
        >>> # El cómputo del subtotal es menor a 500

        Las tuplas de estructura se deben unir por medio de un operador lógico que va
        al principio. Por ejemplo:
        >>> ('amount', '>', 500)
        >>> # El monto es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # El nombre contiene "as"
        >>> 
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # El monto es mayor a 500 y el nombre contiene "as"
        ----

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        ### Desfase de registros para paginación
        Este parámetro sirve para retornar los registros a partir del índice indicado
        por éste. Suponiendo que una búsqueda normal arrojaría los siguientes
        resultados:
        >>> db.search_read(session_uuid, 'base.users')
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   ...
        >>> # ]

        Se puede especificar que el retorno de los registros considerará solo a partir
        desde cierto registro, como por ejemplo lo siguiente:
        >>> db.search_read(session_uuid, 'base.users', offset= 2)
        >>> # [
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   {'id': 7, 'name': 'Sarko Zuimx', 'login': 'sarzu', ...},
        >>> #   {'id': 8, 'name': 'Leo Minnix', 'login': 'minnleo', ...},
        >>> #   ...
        >>> # ]

        ### Límite de registros retornados para paginación
        También es posible establecer una cantidad máxima de registros desde la base de
        datos. Suponiendo que una búsqueda normal arrojaría los siguientes registros:
        >>> db.search_read(session_uuid, 'base.users')
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   ...
        >>> # ]

        Se puede especificar que solo se requiere obtener una cantidad máxima de
        registros a partir de un número provisto:
        >>> db.search_read(session_uuid, 'base.users', limit= 3)
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm', ...},
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...}
        >>> # ]

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.
        :fields: Declaración de campos a leer.
        :offset: Desfase de resultados retornados.
        :limit: Límite de cantidad de resultados retornados.
        :sortby: Nombre o nombres de campo a usar para ordenar los registros.
        :ascending: Dirección de ordenamiento, ascendente (*True*) o descendente
        (*False*).

        **Retorna**

        :records: Lista de diccionarios con los datos de los registros solicitados.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> list[_Record]:
            # Obtención de los datos
            closure_data = self._crud.search_read(
                execution_ctx,
                model_name,
                search_criteria,
                fields,
                offset,
                limit,
                sortby,
                ascending,
            )

            return closure_data

        # Ejecución de la transacción
        data = self.execute_transaction(session_uuid, transaction)

        return data

    def search_count(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        search_criteria: CriteriaStructure[_M] = [],
    ) -> int:
        """
        ## Conteo de búsqueda
        Este método retorna el conteo de de todos los registros de un modelo o los
        registros que cumplan con la condición de búsqueda provista, ideal para
        funcionalidades de paginación que muestran un total de registros.

        Uso:
        >>> # Ejemplo 1
        >>> db.search_count(session_uuid, 'base.users')
        >>> # 5
        >>> 
        >>> # Ejemplo 2
        >>> db.search_count(session_uuid, 'base.permissions', [('create_uid', '=', 5)])
        >>> # 126

        Pueden buscarse registros que cumplan múltiples condiciones:
        >>> db.search(
        >>>     session_uuid,
        >>>     'base.users',
        >>>     [
        >>>         # Las siguientes dos condiciones deben cumplirse
        >>>         '&',
        >>>             # La ID del usuario creador es igual a 2
        >>>             ('create_uid.id', '=', 2),
        >>>             # Nombre de inicio de sesión comienza con "as"
        >>>             ('login', 'starts with', 'as'),
        >>>     ]
        >>> )
        >>> # 2

        Pueden usarse cadenas de atributos en campos de tipo `many2one`:
        >>> db.search(
        >>>     session_uuid,
        >>>     # Modelo de eventos de asistencia de empleados
        >>>     'assistance.registry.event',
        >>>     # La ubicación designada del empleado está activa
        >>>     [('employee_id.location_id.active', '=', True)]
        >>> )
        >>> # 136

        También pueden usarse cómputos de campo:
        >>> # Función de cómputo
        >>> def compute_total(ctx: Lylac.ComputeContext):
        >>>     total = ctx['subtotal'] * (ctx['tax_id.amount'] + 1)
        >>>     return total
        >>> 
        >>> # Cómputo de campo
        >>> line_total = ('total', 'float', compute_total)
        >>> 
        >>> db.search(
        >>>     session_uuid,
        >>>     'sale.order.line',
        >>>     # El subtotal más el monto del impuesto es mayor a $150.00
        >>>     [(line_total, '>', 150)],
        >>> )
        >>> # 215

        ### Estructura de criterio de búsqueda
        La estructura del criterio de búsqueda expresa un conjunto de condiciones que
        se pueden usar para filtrar registros en la base de datos al momento de leer o
        invocar registros para un fin específico.

        La estructura se conforma de un iterable con los tipos:
        - `TripletStructure`: Tupla de 3 posiciones que representa una condición.
        - `LogicOperator`: Operador lógico que une tripletas de condiciones.

        ----

        #### Estructura de tripletas de condición
        Este tipo de dato representa una condición para usarse en una transacción en
        base de datos.

        La estructura de una tripleta consiste en 3 diferentes parámetros:
        1. Referencia de campo. Puede ser alguno de los siguientes tipos:
            - `FieldName`: Nombre del campo del modelo o referencia *Many2One*
            - `FieldComputation`: Cómputo de campo.
        Nombre del campo del modelo, referencia many2one o campo computado
        2. Operador de comparación. Puede ser alguno de los siguientes literales:
            - `'='`: Igual a
            - `'!='`: Diferente de
            - `'=?'`: No está establecido o es igual a
            - `'>'`: Mayor a
            - `'>='`: Mayor o igual a
            - `'<'`: Menor que
            - `'<='`: Menor o igual que
            - `'in'`: Está en
            - `'not in'`: No está en
            - `'like'`: Contiene (sensible a mayúsculas y minúsculas)
            - `'ilike'`: Contiene (no sensible a mayúsculas y minúsculas)
            - `'not like'`: No contiene (sensible a mayúsculas y minúsculas)
            - `'not ilike'`: No contiene (no sensible a mayúsculas y minúsculas)
            - `'starts with'`: Comienza con (sensible a mayúsculas y minúsculas)
            - `'ends with'`: Termina con (sensible a mayúsculas y minúsculas)
            - `'~'`: Coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `'~*'`: Coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
            - `!'~'`: No coincide con expresión regular (sensible a mayúsculas y
            minúsculas)
            - `!'~*'`: No coincide con expresión regular (no sensible a mayúsculas y
            minúsculas)
        3. Valor de comparación. Puede ser alguno de los siguientes tipos:
            - `ScalarOrIterable[DMLScalarCompatible]`Escalar o iterable de Tipo de dato
            que se puede usar como valor para un campo de modelo. El tipo de dato puede
            ser:
                - `int`
                - `float`
                - `str`
                - `bool`
                - `datetime.date`
                - `datetime.datetime`
                - `datetime.time`
                - `datetime.timedelta`
                - `None`
            - `ValueResolutionFn[_M]`: Función de resolución de valor que se usa para
            resolver y retornar un valor que se usará en el campo para almacenarse en
            la base de datos

        Algunos ejemplos de tripletas:
        >>> ('name', 'like', 'Onnymm')
        >>> # El nombre contiene 'Onnymm'
        >>> ('id', '=', 5)
        >>> # La ID es igual a 5
        >>> ('create_uid.name', 'ends with', 'Azzur')
        >>> # El nombre del usuario creador del registro termina con "Azzur"
        >>> ('device_id.type_id.create_date', '=', lambda ctx: ctx.today())
        >>> # La fecha de creación del tipo de dispostivo del dispositivo es igual a hoy
        >>> (('subtotal', 'float', lambda ctx: ctx['qty'] * ctx['price']), '<', 500)
        >>> # El cómputo del subtotal es menor a 500

        Las tuplas de estructura se deben unir por medio de un operador lógico que va
        al principio. Por ejemplo:
        >>> ('amount', '>', 500)
        >>> # El monto es mayor a 500
        >>> ('name', 'ilike', 'as')
        >>> # El nombre contiene "as"
        >>> 
        >>> ['&', ('amount', '>', 500), ('name', 'ilike', 'as')]
        >>> # El monto es mayor a 500 y el nombre contiene "as"
        ----

        #### Operador lógico
        Tipo de dato que representa un operador lógico.

        Los operadores lógicos disponibles son:
        - `'&'`: AND
        - `'|'`: OR

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :search_criteria: Criterio de búsqueda.

        **Retorna**

        :count: Total de registros encontrados.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> int:
            # Obtención del conteo
            closure_count = self._crud.search_count(
                execution_ctx,
                model_name,
                search_criteria,
            )

            return closure_count

        # Ejecución de la transacción
        count = self.execute_transaction(session_uuid, transaction)

        return count

    def update(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        record_ids: ScalarOrIterable[int],
        data: InputRecordData[_M],
    ) -> Literal[True]:
        """
        ## Actualización de registros
        Este método realiza la actualización de uno o más registros a partir de su
        respectiva ID provista, actualizando uno o más campos con el valor provisto.
        Este método solo sobreescribe un mismo valor por cada campo a todos los
        registros provistos.

        Uso:
        >>> db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
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
        >>> db.update(session_uuid, 'base.users', [3, 4, 5], {'name': 'Cambiado'})
        >>> # True
        >>> 
        >>> db.search_read(session_uuid, 'base.users', fields= ['login', 'name'])
        >>> # [
        >>> #   {'id': 2, 'name': 'Onnymm Azzur', 'login': 'onnymm'},
        >>> #   {'id': 3, 'name': 'Cambiado', 'login': 'lumii'},
        >>> #   {'id': 4, 'name': 'Cambiado', 'login': 'meshkim'},
        >>> #   {'id': 5, 'name': 'Cambiado', 'login': 'luunafio'},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu'},
        >>> #   ...
        >>> # ]

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o iterable de IDs de los registros a actualizar.
        :data: Diccionario o iterable de diccionarios de los datos a crear.

        **Retorna**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> Literal[True]:
            # Modificación de los registros
            closure_result = self._crud.update(
                execution_ctx,
                model_name,
                record_ids,
                data,
            )

            return closure_result

        # Ejecución de la transacción
        result = self.execute_transaction(session_uuid, transaction)

        return result

    def delete(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        record_ids: ScalarOrIterable[int],
    ) -> Literal[True]:
        """
        ## Eliminación de registros
        Este método realiza la eliminaciónd e uno o más registros de la base de datos a
        partir de su respectiva ID provista.

        Uso:
        >>> db.search_read(session_uuid, 'base.users')
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
        >>> db.delete(session_uuid, 'base.users', 2)
        >>> # True
        >>> 
        >>> db.search_read(session_uuid, 'base.users')
        >>> # [
        >>> #   {'id': 3, 'name': 'Lumii Mynx', 'login': 'lumii', ...},
        >>> #   {'id': 4, 'name': 'Kim Mesh', 'login': 'meshkim', ...},
        >>> #   {'id': 5, 'name': 'Fioriss Luuna', 'login': 'luunafio', ...},
        >>> #   {'id': 6, 'name': 'Zaylu Bettel', 'login': 'zaylu', ...},
        >>> #   ...
        >>> # ]

        **Parámetros**

        :session_uuid: UUID de sesión.
        :model_name: Nombre de modelo en la base de datos.
        :record_ids: ID o iterable de IDs de los registros a eliminar.

        **Retorna**

        :response: Respuesta de que la operación se realizó correctamente.
        """

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> Literal[True]:
            # Eliminación de los registros
            closure_result = self._crud.delete(
                execution_ctx,
                model_name,
                record_ids,
            )

            return closure_result

        # Ejecución de la transacción
        result = self.execute_transaction(session_uuid, transaction)

        return result

    def authenticate_user(
        self,
        session_uuid: str,
    ) -> int:
        """
        ## Autenticación de usuario
        Este método recibe una UUID de sesión y resuelve a qué usuario le pertenece la
        sesión.

        Uso:
        >>> session_uuid = '4d9ad73f-40cf-4b33-8feb-4c593c172cf2'
        >>> 
        >>> db.authenticate_user(session_uuid)
        >>> # 2

        **Parámetros**

        :session_uuid: UUID de sesión.

        **Retorna**

        :user_id: ID del usuario propietario de la sesión.
        """

        # Construcción de función de autenticación de usuario
        transaction = build_authenticate_user_callback(self, session_uuid)
        # Obtención de la UID de usuario autenticado
        uid = self._engine.execute_complex(transaction)

        return uid

    def _load_from_built_database(
        self,
    ) -> None:

        # Obtención de metadatos de la base de datos
        self._get_metadata()
        # Inicialización de instancia en base a base de datos existente
        self._engine.execute_complex(self._ddl.rebuild_from_existing_database)
        # Inicialización de motores
        self._initialize_engines()
        # Construccción de centros de motores
        self._build_hubs()
        # Se indica que no es la primera inicialización en la base de datos
        self._is_first_initialization = False

    def _build_database_structure(
        self,
        build_models_fn: ExecutableTransactionCallback[_M],
    ) -> None:

        # Se intenta inicializar la instancia construyendo la base de datos
        try:
            # Inicialización desde cero
            self._build_database()
            # Construccción de centros de motores
            self._build_hubs()
            # Ejecución de construcción de datos internos
            self._execute_as_root(build_database_structure)
            # Ejecución de la función provista para la construcción personalizada de la base de datos
            self._execute_as_root(build_models_fn)
            # Se indica que es la primera inicialización en la base de datos
            self._is_first_initialization = True

        # Si ocurre algún error...
        except Exception:
            # Se deshace la construcción de la base de datos
            _Base.metadata.drop_all(self._engine._engine)
            # Se arroja el error
            raise

        # Se indica que la inicialización se realizó correctamente
        print(MONITOR.INITIALIZATION_FINISHED)

    def _build_hubs(
        self,
    ) -> None:

        # Construcción de centro de automatizaciones
        self._automations.build_hub(self._metadata)
        # Construcción de centro de acciones
        self._actions.build_hub(self._metadata)
        # Construcción de centro de campos computados
        self._compute.expand_to_custom_models(self._metadata)
        # Construcción de centro de campos validaciones
        self._validations.build_hub(self._metadata)
        # Construcción de centro de políticas
        self._policies.build_hub(self._metadata)

    def _build_database(
        self,
    ) -> None:

        # Creación de las tablas y los campos base con ayuda de las utilidades de SQLAlchemy
        _Base.metadata.create_all(self._engine._engine)
        # Inicialización de motores
        self._initialize_engines()
        # Construcción de los datos base iniciales
        self._build_initial_base_data()

        # Instalación de paquetes iniciales
        for package_name in INITIAL_PACKAGES:
            self.modules.install(package_name)

        # Obtención de metadatos de la base de datos
        self._get_metadata()

    def _initialize_engines(
        self,
    ) -> None:

        # Inicialización de motor de acciones
        self._actions = ActionEngine[_M](self._ddl, self._crud)
        # Inicialización de motor de automatizaciones
        self._automations = AutomationsEngine[_M](self._ddl, self._crud)
        # inicialización de motor de cómputo de campos
        self._compute = ComputeEngine[_M]()
        # Inicialización de motor de políticas
        self._policies = PoliciesEngine[_M](self._crud)
        # Inicialización de motor de tareas de servidor
        self._server_tasks = ServerTasksEngine[_M](self._crud)
        # Inicialización de motor de validaciones
        self._validations = ValidationEngine[_M](self._crud)
        # Inicialización de motor de valores de usuario
        self._user_env = UserEnvEngine[_M](self._crud)

        # Inicialización de API de extensión
        self.api = _MainAPI[_M](
            automations= self._automations,
            validations= self._validations,
            actions= self._actions,
            compute= self._compute,
            policies= self._policies,
            server_tasks= self._server_tasks,
            user_env= self._user_env,
            crud= self._crud,
            main= self,
        )

    def _get_metadata(
        self,
    ) -> None:

        # Ejecución de función de construcción de metadatos desde la base de datos
        self._engine.execute_complex(self._metadata.build)

    def _execute_as_root(
        self,
        execution_callback: Callable[[_TransactionContext[_M]], None],
    ) -> None:

        # Definición de la transacción
        def transaction(conn: Connection) -> None:
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_root_execution_context(conn)
            # Inicialización de contexto de transacción
            transaction_ctx = _TransactionContext(execution_ctx)
            # Ejecución de la función provista
            execution_callback(transaction_ctx)

            # Se realiza commit
            execution_ctx.commit()

        # Ejecución de la función de transacción
        self._engine.execute_complex(transaction)

    def _build_initial_base_data(
        self,
    ) -> None:

        # Definición de la transacción
        def transaction(ctx: _TransactionContext[_M]):
            # Obtención de mapa de datos
            data_map = build_initial_data(ctx.conn)

            # Creación de datos
            ctx.create(MODEL_NAME.BASE_MODEL_DATA, data_map.model_data)
            ctx.create(MODEL_NAME.BASE_MODEL_DATA_PROCESS, data_map.process)
            ctx.create(MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP, data_map.steps)
            ctx.create(MODEL_NAME.BASE_MODEL_DATA_PROCESS_STEP_RECORD, data_map.total_records)

        # Ejecución de la transacción
        self._execute_as_root(transaction)

    def _create_root_execution_context(
        self,
        conn: Connection,
    ) -> _ExecutionContext[_M]:

        # Creación de un contexto de ejecución como usuario root
        execution_ctx = self._create_execution_context(REF.BASE_USERS.ROOT_USER, conn)

        return execution_ctx

    def _create_execution_context(
        self,
        uid: int,
        conn: Connection,
    ) -> _ExecutionContext[_M]:

        # Creación de un contexto de ejecución
        execution_ctx = _ExecutionContext[_M](
            crud= self._crud,
            uid= uid,
            conn= conn,
            models_bearer= self._models_bearer,
            database_metadata= self._metadata,
            compute= self._compute,
            automations= self._automations,
            validations= self._validations,
            policies= self._policies,
            actions= self._actions,
            server_tasks= self._server_tasks,
            user_env_engine= self._user_env,
            notifier_init= self._notifier_init,
        )

        return execution_ctx
