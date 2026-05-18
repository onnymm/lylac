from typing import Callable
from typing import Generic
from .._constants import ERROR_LABEL
from .._contexts import ValidationContext as ValidationContext
from .._contracts import _Contract_CRUD
from .._contracts.contexts import Contract_ExecutionContext
from .._data import PRESET_VALIDATIONS
from .._errors import ValidationExecutionError
from .._resources import DatabaseMetadata
from .._resources import ErrorDetail
from .._resources import InputParser
from .._resources import Slot
from .._resources import ValidationProperties
from .._typing.callables import ValidationCallback
from .._typing.generics import ItemOrList
from .._typing.generics import ModelName
from .._typing.literals import TTypeName
from .._typing.literals import DMLTransaction
from .._typing.structures import RecordData
from .._typing.type_parameters import _M

class TRANSACTION_NAME:
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

TRANSACTIONS = [
    TRANSACTION_NAME.CREATE,
    TRANSACTION_NAME.UPDATE,
    TRANSACTION_NAME.DELETE,
]

class ValidationEngine(Generic[_M]):
    _preset_validations: list[ValidationProperties[_M]] = PRESET_VALIDATIONS

    def __init__(
        self,
        crud: _Contract_CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        # Inicialización de estado del motor
        self._active = False
        # Inicialización de centro de validaciones
        self._hub = Slot[_M, ValidationProperties[_M]]()

    def build_hub(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:

        # Iteración por los nombres de transacción
        for transaction in TRANSACTIONS:
            # Inicialización de diccionario de validaciones globales én el diccionario de transacción
            self._hub[transaction][None] = {}
            # Iteración por los nombres de modelo
            for model_name in database_metadata.model_names:
                # Inicialización de diccionario de validaciones por modelo
                self._hub[transaction][model_name] = {}

        # Iteración por las propiedades de validaciones predeterminadas
        for validation_properties in self._preset_validations:
            # Obtención del nombre de la función de validación
            callback_name = validation_properties.callback.__name__
            # Obtención de nombre de modelo de la validación
            model_name = validation_properties.model_name

            # Si la validación pertenecerá a más de una transacción...
            if isinstance(validation_properties.transaction, list):
                # Obtención de los nombres de transacción
                transactions = validation_properties.transaction
                # Iteración por cada transacción
                for transaction in transactions:
                    # Registro de las propiedades de validación por la transacción y el nombre del modelo
                    self._hub[transaction][model_name][callback_name] = validation_properties

            # Si la validación no pertenecerá a más de una transacción...
            else:
            # Registro de las propiedades de validación por la transacción y el nombre del modelo
                self._hub[validation_properties.transaction][model_name][callback_name] = validation_properties

        # Se activa el motor de validaciones
        self._active = True

    def validate(
        self,
        on: DMLTransaction,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        records: list[RecordData],
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
        parsed_records = [parser.parse(record) for record in records]

        # Obtención de centro de validaciones del tipo de transacción correspondiente
        hub = self._hub[on]

        # Obtención de las validaciones
        validations_properties = [
            *hub[None].values(), 
            *hub[model_name].values(),
        ]

        # Inicialización de lista de detalles de error
        errors: list[ErrorDetail] = []

        # Iteración por las propiedades de validaciones
        for validation_properties in validations_properties:
            # Inicialización del contexto de validación
            ctx = ValidationContext[_M](
                execution_ctx,
                self._crud,
                model_name,
                parsed_records.copy(),
                errors,
                validation_properties.message,
            )

            # Ejecución de la validación
            validation_properties.callback(ctx)

        # Si fueron encontrados errores...
        if errors:
            # Iteración por cada error
            for error in errors:
                # Se imprime éste
                print(error)
            # Se lanza error para detener la ejecución
            raise AssertionError('Las validaciones no pasaron.')

    def register(
        self,
        on: ItemOrList[DMLTransaction],
        model_name: ModelName[_M],
        message: str,
    ) -> Callable[[ValidationCallback[_M]], ValidationCallback[_M]]:

        # Inicialización de decorador
        def decorator(callback: ValidationCallback[_M]):

            # Obtención del nombre de la función
            callback_name = callback.__name__

            # Inicialización de propiedades de la validación
            validation_properties = ValidationProperties[_M](
                on,
                callback,
                message,
                model_name,
            )

            # Si existe más de una transacción...
            if isinstance(on, list):
                for transaction in on:
                    # Registro de las propiedades de la validación
                    self._hub[transaction][model_name][callback_name] = validation_properties

            # Si noexiste más de una transacción...
            else:
                # Registro de las propiedades de la validación
                self._hub[on][model_name][callback_name] = validation_properties

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
            # Inicialización de diccionario de validaciones por el modelo
            self._hub[transaction][model_name] = {}

    def _build_void_function(
        self,
    ) -> ValidationCallback[_M]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(ctx: ValidationContext[_M]) -> None:
            # Se lanza error de ejecución
            raise ValidationExecutionError(ERROR_LABEL.MANUAL_VALIDATION)

        return void_function

    def _get_ttypes(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
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
        fields_ttypes: dict[str, TTypeName] = {record['name']: record['ttype'] for record in found_results}

        return fields_ttypes
