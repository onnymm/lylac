from typing import Callable
from typing import Generic
from typing import TYPE_CHECKING
from .._constants import ERROR_LABEL
from .._constants import TRANSACTIONS
from .._contexts import PoliciesContext
from .._data import PRESET_POLICIES
from .._resources import DatabaseMetadata
from .._resources import ErrorDetail
from .._resources import InputParser
from .._resources import PolicyProperties
from .._resources import Slot
from .._typing.callables import PolicyCallback
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.generics import _Record
from .._typing.literals import TTypeName
from .._typing.literals import DMLTransaction
from .._typing.structures import RecordData
from .._typing.type_parameters import _M
from .._typing.type_parameters import _R
from ..errors import PolicyExecutionError

if TYPE_CHECKING:
    from .._contexts import ExecutionContext
    from .._contexts import PoliciesContext
    from .._orchestrator import CRUD

class PoliciesEngine(Generic[_M, _R]):

    def __init__(
        self,
        crud: CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        # Inicialización de estado del motor
        self._active = False
        # Inicialización de centro de políticas
        self._hub = Slot[_M, PolicyProperties[_M]]()
        # Obtención de las políticas predeterminadas
        self._preset_policies = PRESET_POLICIES.copy()

    def build_hub(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:

        # Iteración por los nombres de transacción
        for transaction in TRANSACTIONS:
            # Inicialización de diccionario de políticas globales én el diccionario de transacción
            self._hub[transaction][None] = {}
            # Iteración por los nombres de modelo
            for model_name in database_metadata.model_names:
                # Inicialización de diccionario de políticas por modelo
                self._hub[transaction][model_name] = {}

        # Iteración por las propiedades de políticas predeterminadas
        for policy_properties in self._preset_policies:
            # Obtención del nombre de la función de verificación
            callback_name = policy_properties.callback.__name__
            # Obtención de nombre de modelo de la verificación
            model_name = policy_properties.model_name

            # Si la política pertenecerá a más de una transacción...
            if isinstance(policy_properties.transaction, list):
                # Obtención de los nombres de transacción
                transactions = policy_properties.transaction
                # Iteración por cada transacción
                for transaction in transactions:
                    # Registro de las propiedades de política por la transacción y el nombre del modelo
                    self._hub[transaction][model_name][callback_name] = policy_properties

            # Si la política no pertenecerá a más de una transacción...
            else:
            # Registro de las propiedades de política por la transacción y el nombre del modelo
                self._hub[policy_properties.transaction][model_name][callback_name] = policy_properties

        # Se activa el motor de políticas
        self._active = True

    def verify_incoming_ids(
        self,
        on: DMLTransaction,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        records_ids: list[int],
    ) -> None:

        # Lectura de datos
        data = execution_ctx.read(model_name, records_ids)

        # Verificación de los datos
        self._verify(
            on,
            execution_ctx,
            model_name,
            data,
        )

    def verify_incoming_data(
        self,
        on: DMLTransaction,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        data: list[RecordData],
    ) -> None:

        # Si el motor no está encendido aún...
        if not self._active:
            # Se termina la ejecución
            return

        # Obtención de los tipos de datos de los campos del modelo
        ttypes = self._get_ttypes(execution_ctx, model_name)
        # Inicialización de instancia de parseador de datos de entrada
        parser = InputParser(ttypes)
        # Parseo de registros
        parsed_records = [parser.parse(record) for record in data]

        # Verificación de los datos
        self._verify(
            on,
            execution_ctx,
            model_name,
            parsed_records,
        )

    def register(
        self,
        on: ItemOrList[DMLTransaction],
        model_name: ModelName[_M],
        message: str,
    ) -> Callable[[PolicyCallback[_M]], PolicyCallback[_M]]:

        # Inicialización de decorador
        def decorator(callback: PolicyCallback[_M]):

            # Obtención del nombre de la función
            callback_name = callback.__name__

            # Inicialización de propiedades de la política
            policy_properties = PolicyProperties[_M](
                on,
                callback,
                message,
                model_name,
            )

            # Si existe más de una transacción...
            if isinstance(on, list):
                for transaction in on:
                    # Registro de las propiedades de la política
                    self._hub[transaction][model_name][callback_name] = policy_properties

            # Si noexiste más de una transacción...
            else:
                # Registro de las propiedades de la política
                self._hub[on][model_name][callback_name] = policy_properties

            # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
            replaced_function = self._build_void_function()

            return replaced_function

        return decorator

    def add(
        self,
        model_name: ModelName[_M],
    ) -> None:

        # Iteración por los nombres de transacción
        for transaction in TRANSACTIONS:
            # Inicialización de diccionario de políticas por el modelo
            self._hub[transaction][model_name] = {}

    def _verify(
        self,
        on: DMLTransaction,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
        data: list[_Record],
    ) -> None:

        # Obtención de centro de políticas del tipo de transacción correspondiente
        hub = self._hub[on]

        # Obtención de las políticas
        policies_properties = [
            *hub[None].values(),
            *hub[model_name].values(),
        ]

        # Inicialización de lista de detalles de error
        errors: list[ErrorDetail] = []

        # Iteración por las propiedades de políticas
        for policy_properties in policies_properties:
        # Creación de contexto de políticas
            ctx = PoliciesContext(
                execution_ctx,
                self._crud,
                model_name,
                data,
                errors,
                policy_properties.message,
            )

            # Ejecución de la verificación
            policy_properties.callback(ctx)

        # Si fueron encontrados errores...
        if errors:
            # Iteración por cada error
            for error in errors:
                # Se imprime éste
                print(error)
            # Se lanza error para detener la ejecución
            raise AssertionError('Las verificaciones no pasaron.')

    def _build_void_function(
        self,
    ) -> PolicyCallback[_M]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(ctx: PoliciesContext[_M]) -> None:
            # Se lanza error de ejecución
            raise PolicyExecutionError(ERROR_LABEL.MANUAL_POLICY)

        return void_function

    def _get_ttypes(
        self,
        execution_ctx: ExecutionContext[_M],
        model_name: ModelName[_M],
    ) -> dict[str, TTypeName]:

        # Búsqueda y lectura de los campos del modelo
        found_results = self._crud.search_read(
            execution_ctx,
            'base.model.field',
            [('model_id.model', '=', model_name)],
            ['name', 'ttype'],
        )

        # Mapeo de tipos de dato
        fields_ttypes: dict[str, TTypeName] = {
            record['name']: record['ttype']
            for record
            in found_results
        }

        return fields_ttypes
