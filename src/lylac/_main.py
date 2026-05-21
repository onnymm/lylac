from datetime import datetime
from datetime import timedelta
from typing import Any
from typing import Callable
from typing import Generic
from typing import Literal
from typing import Optional
from typing import Union
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.engine import Connection
from ._api import _MainAPI
from ._constants import DATA_RESOURCE
from ._constants import ERROR_LABEL
from ._constants import INITIAL_PACKAGES
from ._contexts import ActionContext as _ActionContext
from ._contexts import AutomationContext as _AutomationContext
from ._contexts import ComputeContext as _ComputeContext
from ._contexts import ExecutionContext as _ExecutionContext
from ._contexts import ValidationContext as _ValidationContext
from ._contexts import ServerTaskContext as _ServerTaskContext
from ._contexts import TransactionContext as _TransactionContext
from ._core import Metadata
from ._core import Transaction
from ._core.models import _Base
from ._data import build_database_structure
from ._data import build_initial_data
from ._engines import ActionEngine
from ._engines import AutomationsEngine
from ._engines import ComputeEngine
from ._engines import ServerTasksEngine
from ._engines import UserEnvEngine
from ._engines import ValidationEngine
from ._errors import ExpiredSessionError
from ._errors import IncorrectPasswordError
from ._errors import InvalidSessionUUIDError
from ._errors import UserNotActiveError
from ._errors import UserNotFoundError
from ._operations import DDL
from ._orchestrator import CRUD
from ._resources import DatabaseMetadata
from ._resources import ModelDataIndex
from ._resources import ModelsBearer
from ._services import ConnectionService
from ._typing.callables import ExecutableTransactionCallback
from ._typing.callables import ComputeFieldFn as _ComputeFieldFn
from ._typing.generics import ItemOrList
from ._typing.generics import ModelName
from ._typing.generics import _Record
from ._typing.generics import _Records
from ._typing.models import _base_users__fields
from ._typing.models import _found_session
from ._typing.structures import RecordData
from ._typing.structures import RecordData
from ._typing.structures import RecordData
from ._typing.structures import CriteriaStructure
from ._typing.structures import FieldReadDeclaration
from ._typing.type_parameters import _M
from ._typing.type_parameters import _R
from ._typing.type_parameters import _T
from .security import verify_password
from sqlalchemy.exc import ProgrammingError

class Lylac(Generic[_M]):
    _is_first_initialization: bool
    # Interfaz para acceso al tipado de automatización sin tener que colocar literal de modelos
    type AutomationContext[T] = _AutomationContext[_M, T]
    type ValidationContext[T] = _ValidationContext[_M, T]
    type ActionContext[T] = _ActionContext[_M, Union[T, _R]]
    type ServerTaskContext = _ServerTaskContext[_M]
    type TransactionContext = _TransactionContext[ModelName[_M]]
    type ExecutionContext = _ExecutionContext[_M]
    type ComputeContext = _ComputeContext[_M]
    type ComputeFieldFn = _ComputeFieldFn[_M]

    def __init__(
        self,
        build_models_fn: ExecutableTransactionCallback = lambda _: None,
        populate_models_fn: ExecutableTransactionCallback = lambda _: None,
    ) -> None:

        # Asignación de valores
        self._populate_models_fn = populate_models_fn

        # Inicialización de instancia de servicio de conexión a la base de datos
        self._connection = ConnectionService()
        # inicialización de instancia de portador de modelos
        self._models_bearer = ModelsBearer[_M]()
        # Inicialización de instancia de transacciones especiales
        self._transaction = Transaction()
        # Inicialización de instancia de metadatos de la base de datos
        self._metadata = DatabaseMetadata()
        # Inicialización de orquestador CRUD
        self._crud = CRUD(self._models_bearer)
        # Inicialización de instancia de operaciones DDL
        self._ddl = DDL(self._models_bearer, self._metadata)

        # Se intenta inicializar la instancia con datos existentes
        try:
            # Inicialización desde datos existentes de la base de datos
            self._load_from_built_database()
            # Construccción de centros de motores
            self._build_hubs()
            # Se indica que no es la primera inicialización en la base de datos
            self._is_first_initialization = False

        except ProgrammingError as e:
            # Se intenta inicializar la instancia construyendo la base de datos
            try:
                # Inicialización desde cero
                self._build_database()
                # Construccción de centros de motores
                self._build_hubs()
                # Se indica que es la primera inicialización en la base de datos
                self._is_first_initialization = True
                # Ejecución de construcción de datos internos
                self._execute_as_root(build_database_structure)
                # Ejecución de la función provista para la construcción personalizada de la base de datos
                self._execute_as_root(build_models_fn)

            # Si ocurre algún error...
            except Exception as e:
                # Se deshace la construcción de la base de datos
                _Base.metadata.drop_all(self._connection._engine)
                # Se arroja el error
                raise

            print('Se termina la inicialización correctamente')

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

        # Definición de la transacción
        def transaction(conn: Connection):
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)
            # Se busca el usuario
            found_users: _Records[_base_users__fields] = self._crud.search_read(
                execution_ctx,
                'base.users',
                [('login', '=', username)],
                ['login', 'active', 'password'],
            )

            # Si no se encontró usuario...
            if not found_users:
                # Se arroja error de usuario no encontrado
                raise UserNotFoundError(ERROR_LABEL.USER_NOT_FOUND)

            # Obtención de los datos del usuario
            [ user_data ] = found_users

            # Si el usuario no está activo...
            if not user_data['active']:
                # Se arroja error de usuario inactivo
                raise UserNotActiveError(ERROR_LABEL.USER_NOT_ACTIVE)

            # Obtención de la contraseña hasheada
            hashed_password: str = user_data['password']
            # Obtención de la ID del usuario
            user_id = user_data['id']

            # Verificación de la contraseña
            is_pwd_correct = verify_password(password, hashed_password)

            # Si la contraseña no es correcta...
            if not is_pwd_correct:
                # Se arroja error de contraseña incorrecta
                raise IncorrectPasswordError(ERROR_LABEL.INCORRECT_PASSWORD)

            # Creación de UUID de sesión
            session_uuid = uuid4().__str__()

            # Creación de sesión de usuario
            self._crud.create(
                execution_ctx,
                'base.user.session',
                {
                    'name': session_uuid,
                    'user_id': user_id,
                    'validity_time': timedelta(days= 30),
                },
            )

            # Se realiza commit
            conn.commit()

            return session_uuid

        # Ejecución de la función de transacción
        session_uuid = self._connection.execute_complex(transaction)

        return session_uuid

    def execute_transaction(
        self,
        session_uuid: str,
        callback: Callable[[_ExecutionContext[_M]], _T],
    ) -> _T:

        # Autenticación del usuario
        uid = self._authenticate_user(session_uuid)

        def wrapped_transaction(conn: Connection) -> _T:
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(session_uuid, uid, conn)
            # Ejecución de la función
            closure_result = callback(execution_ctx)

            return closure_result

        # Ejecución de la función de transacción
        result = self._connection.execute_complex(wrapped_transaction)

        return result

    def execute(
        self,
        session_uuid: str,
        execution_callback: Callable[[_TransactionContext[_M]], None]
    ) -> None:

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> None:
            # Inicialización de contexto de transacción
            transaction_ctx = _TransactionContext(execution_ctx, self._crud)
            # Ejecución de la función provista
            execution_callback(transaction_ctx)

            # Se realiza commit
            execution_ctx.conn.commit()

        # Ejecución de la transacción
        self.execute_transaction(session_uuid, transaction)

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
            # Se guardan los cambios
            execution_ctx.conn.commit()

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
    ) -> list[_Record]:

        # Definición de la transacción
        def transaction(execution_ctx: _ExecutionContext[_M]) -> list[_Record]:
            # Obtención de los datos
            closure_data = self._crud.read(
                execution_ctx,
                model_name,
                record_ids,
                fields,
            )

            return closure_data

        # Ejecución de la transacción
        data = self.execute_transaction(session_uuid, transaction)

        return data

    def search_read(
        self,
        session_uuid: str,
        model_name: ModelName[_M],
        record_ids: ItemOrList[int],
        fields: list[FieldReadDeclaration] = [],
        sortby: Optional[ItemOrList[str]] = None,
        ascending: Optional[ItemOrList[bool]] = None
    ):

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

    def _authenticate_user(
        self,
        session_uuid: str,
    ) -> int:

        # Definición de la transacción
        def transaction(conn: Connection) -> int:
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)

            # Búsqueda y lectura de la sesión
            found: _Records[_found_session] = self._crud.search_read(
                execution_ctx,
                'base.user.session',
                [('name', '=', session_uuid)],
                [
                    ('is_active_session', 'boolean', lambda ctx: ctx['expires_at'] > datetime.now()),
                    ('user_id.id', 'uid'),
                    ('user_id.active', 'user_is_active'),
                ],
            )

            # Si no fue encontrado ningún registro de sesión de usuario...
            if not found:
                # Se arroja error de UUID de sesión inválida
                raise InvalidSessionUUIDError(ERROR_LABEL.INVALID_SESSION_UUID)

            # Obtención del registro de sesión
            [ session_record ] = found

            # Obtención de datos de la sesión
            is_active_session = session_record['is_active_session']
            user_is_active = session_record['user_is_active']
            uid = session_record['uid']

            # Si la sesión ya no está activa...
            if not is_active_session:
                # Se arroja error de sesión expirada
                raise ExpiredSessionError(ERROR_LABEL.EXPIRED_SESSION)

            # Si el usuario no está activo...
            if not user_is_active:
                # Se arroja error de usuario desactivado
                raise UserNotActiveError(ERROR_LABEL.USER_NOT_ACTIVE)

            return uid

        # Obtención de la UID de usuario autenticado
        uid = self._connection.execute_complex(transaction)

        return uid

    def _load_from_built_database(
        self,
    ) -> None:

        # Obtención de metadatos de la base de datos
        self._get_metadata()
        # Inicialización de instancia en base a base de datos existente
        self._connection.execute_complex(self._ddl.rebuild_from_existing_database)
        # Inicialización de motores
        self._initialize_engines()

    def _build_database(
        self,
    ) -> None:

        # Creación de las tablas y los campos base con ayuda de las utilidades de SQLAlchemy
        _Base.metadata.create_all(self._connection._engine)
        # Inicialización de motores
        self._initialize_engines()

        # Construcción de los datos base iniciales
        self._build_initial_base_data()

        # Instalación de paquetes iniciales
        for package in INITIAL_PACKAGES:
            self._install(package)

        # Obtención de metadatos de la base de datos
        self._get_metadata()

    def _initialize_engines(
        self,
    ) -> None:

        # Inicialización de motor de acciones
        self._actions = ActionEngine[_M](self._crud)
        # Inicialización de motor de automatizaciones
        self._automations = AutomationsEngine[_M](self._ddl, self._crud)
        # inicialización de motor de cómputo de campos
        self._compute = ComputeEngine[_M]()
        # Inicialización de motor de tareas de servidor
        self._server_tasks = ServerTasksEngine[_M](self._crud)
        # Inicialización de motor de validaciones
        self._validations = ValidationEngine[_M](self._crud)
        # Inicialización de motor de valores de usuario
        self._user_env = UserEnvEngine[_M](self._crud)

        # Inicialización de API de extensión
        self.api = _MainAPI(
            automations= self._automations,
            validations= self._validations,
            actions= self._actions,
            compute= self._compute,
            server_tasks= self._server_tasks,
            user_env= self._user_env,
            main= self,
        )

    def _get_metadata(
        self,
    ) -> None:

        # Ejecución de función de construcción de metadatos desde la base de datos
        self._connection.execute_complex(self._metadata.build)

    def _create_execution_context(
        self,
        session_uuid: str,
        uid: int,
        conn: Connection,
    ) -> _ExecutionContext[_M]:

        # Creación de un contexto de ejecución
        execution_ctx = _ExecutionContext[_M](
            session_uuid,
            self._crud,
            uid,
            conn,
            self._models_bearer,
            self._metadata,
            self._compute,
            self._automations,
            self._validations,
            self._actions,
            self._user_env,
        )

        return execution_ctx

    def _execute_as_root(
        self,
        execution_callback: Callable[[_TransactionContext[_M]], None],
    ) -> None:

        # Definición de la transacción
        def transaction(conn: Connection) -> None:
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)
            # Inicialización de contexto de transacción
            transaction_ctx = _TransactionContext(execution_ctx, self._crud)
            # Ejecución de la función provista
            execution_callback(transaction_ctx)

            # Se realiza commit
            execution_ctx.conn.commit()

        # Ejecución de la función de transacción
        self._connection.execute_complex(transaction)

    def _install(
        self,
        process_name: str,
    ) -> None:

        # Función de transacción
        def transaction(conn: Connection):

            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)

            # Inicialización de instancia de índice de datos de modelo
            model_data_index = ModelDataIndex(conn)

            # Query para encontrar proceso en base a su nombre
            stmt_find_process_by_name = (
                # Se selecciona únicamente la ID
                select(Metadata.BaseModelDataProcess.id)
                # Búsqueda por coincidencia exacta del nombre provisto
                .where(Metadata.BaseModelDataProcess.name == process_name)
            )
            # Obtención de la ID del proceso a ejecutar
            [ process_id ] = self._transaction.search(stmt_find_process_by_name, conn)

            # Query para encontrar los pasos del proceso
            stmt_find_process_steps = (
                select(
                    # Selección de ID y nombre del modelo relacionado
                    Metadata.BaseModelDataProcessStep.id,
                    Metadata.BaseModelDataProcessStep.model_name,
                )
                # Búsqueda por pasos que pertenezcan al proceso en cuestión
                .where(Metadata.BaseModelDataProcessStep.process_id == process_id)
            )

            # Obtención de los datos de los pasos del proceso
            steps_data: list[tuple[int, ModelName[_M]]] = self._transaction.search_read(stmt_find_process_steps, conn)

            # Iteración por los datos de cada paso del proceso
            for step_data in steps_data:
                # Destructuración de ID y nombre de modelo desde los datos del paso del proceso
                ( step_id, step_model ) = step_data

                # Query para encontrar los registros que pertenecen al paso del proceso
                stmt_find_step_records_ordered_by_sequence = (
                    select(
                        # Selección de nombre y datos en formato JSON parseados a diccionario
                        Metadata.BaseModelDataProcessStepRecord.name,
                        Metadata.BaseModelDataProcessStepRecord.data,
                    )
                    # Filtro por los registros que pertenecen al paso del proceso
                    .where(Metadata.BaseModelDataProcessStepRecord.step_id == step_id)
                    # Ordenamiento de forma ascendente
                    .order_by(Metadata.BaseModelDataProcessStepRecord.sequence)
                )

                # Obtención de los datos de los registros
                records_data = self._transaction.search_read(stmt_find_step_records_ordered_by_sequence, conn)

                # Inicialización de lista de diccionarios de datos a crear en la base de datos
                data_to_create: list[dict[str, Any]] = []
                # Inicialización de lista de referencias a datos de modelo
                model_data_refs: list[str] = []

                # Iteración por cada registro de datos de registros
                for record_data in records_data:
                    # Destructuración de la referencia de datos y los datos
                    ( model_data_ref_i, model_data_i ) = record_data

                    # Se añaden la referencia y los datos a sus respectivas listas
                    data_to_create.append(model_data_i)
                    model_data_refs.append(model_data_ref_i)

                # Procesamiento de datos a crear
                processed_data_to_create = model_data_index.process(data_to_create)

                # Creación de los registros dictados por el registro
                created_ids = self._crud.create(execution_ctx, step_model, processed_data_to_create)

                # Iteración por referencia de datos de modelo y registro creado
                for (ref, record_id) in zip(model_data_refs, created_ids):

                    # Query para actualizar los datos del registro de datos de modelo
                    stmt_update_model_data_record = (
                        update(Metadata.BaseModelData)
                        .where(Metadata.BaseModelData.name == ref)
                        .values(res_id = record_id)
                    )
                    # Ejecución de la actualización de los datos del registro de datos del modelo
                    self._transaction.update(stmt_update_model_data_record, conn)

            # Se guardan los cambios en la base de datos
            conn.commit()

        # Ejecución de la transacción construida
        self._connection.execute_complex(transaction)

    def _build_initial_base_data(
        self,
    ) -> None:

        # Definición de la transacción
        def transaction(conn: Connection):
            # Inicialización de contexto de ejecución
            execution_ctx = self._create_execution_context(None, DATA_RESOURCE.ROOT_USER, conn)

            # Obtención de mapa de datos
            data_map = build_initial_data(conn)

            # Creación de datos
            self._crud.create(execution_ctx, 'base.model.data', data_map.model_data)
            self._crud.create(execution_ctx, 'base.model.data.process', data_map.process)
            self._crud.create(execution_ctx, 'base.model.data.process.step', data_map.steps)
            self._crud.create(execution_ctx, 'base.model.data.process.step.record', data_map.total_records)

            # Se realiza commit
            conn.commit()

        # Ejecución de la transacción
        self._connection.execute_complex(transaction)
