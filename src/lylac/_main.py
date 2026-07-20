from typing import Callable
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Union
from sqlalchemy.engine import Connection
from sqlalchemy.exc import ProgrammingError
from ._api import _MainAPI
from ._constants import DATA_RESOURCE
from ._constants import MODEL_NAME
from ._constants import MONITOR
from ._constants import INITIAL_PACKAGES
from ._contexts import ActionContext as _ActionContext
from ._contexts import AutomationContext as _AutomationContext
from ._contexts import ComputeContext as _ComputeContext
from ._contexts import ExecutionContext as _ExecutionContext
from ._contexts import ValidationContext as _ValidationContext
from ._contexts import ServerTaskContext as _ServerTaskContext
from ._contexts import TransactionContext as _TransactionContext
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
from ._services import Notifier
from ._typing.callables import ExecutableTransactionCallback
from ._typing.callables import ComputeFieldFn as _ComputeFieldFn
from ._typing.generics import ItemOrList
from ._typing.generics import ModelName
from ._typing.generics import _Record
from ._typing.structures import CriteriaStructure
from ._typing.structures import RecordData
from ._typing.structures import FieldReadDeclaration
from ._typing.type_parameters import _M
from ._typing.type_parameters import _R
from ._typing.type_parameters import _T
from .security import build_authenticate_user_callback
from .security import build_login_callback

class Lylac(Generic[_M]):
    # Interfaz para acceso al tipado de automatización sin tener que colocar literal de modelos
    type AutomationContext[T] = _AutomationContext[_M, T]
    type ValidationContext[T] = _ValidationContext[_M, T]
    type ActionContext[T] = _ActionContext[_M, Union[T, _R]]
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
        notifier_init: Callable[[_ExecutionContext[_M]], Notifier] = lambda ctx: DefaultNotifier(ctx.uid),
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
        data: ItemOrList[RecordData],
    ) -> list[int]:

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
        search_criteria: CriteriaStructure = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[int]:

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
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:

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
        search_criteria: CriteriaStructure = [],
        fields: list[FieldReadDeclaration] = [],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None,
    ) -> list[_Record]:

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
        search_criteria: CriteriaStructure = [],
    ) -> int:

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
        record_ids: ItemOrList[int],
        data: dict,
    ) -> Literal[True]:

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
        record_ids: ItemOrList[int],
    ) -> Literal[True]:

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
        execution_ctx = self._create_execution_context(DATA_RESOURCE.ROOT_USER, conn)

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
