from typing import Callable
from typing import Generic
from typing import TYPE_CHECKING
from .._constants import FIELD_NAME
from .._constants import ERROR_LABEL
from .._contexts import AutomationContext
from .._contracts import _Contract_CRUD
from .._data._preset_automations import DEFAULT_ON_CREATE_AUTOMATIONS
from .._resources import AutomationProperties
from .._resources import Slot
from .._resources import DatabaseMetadata
from .._typing.callables import AutomationCallback
from .._typing.callables import CaptureIDsAfterDeletionFn
from .._typing.generics import FunctionDecorator
from .._typing.generics import ModelName
from .._typing.generics import EngineHub
from .._typing.literals import DMLTransaction
from .._typing.structures import CriteriaStructure
from .._typing.structures import FieldReadDeclaration
from .._typing.type_parameters import _M
from .._contracts.contexts import Contract_ExecutionContext
from ..errors import AutomationExecutionError

if TYPE_CHECKING:
    from .._operations import DDL

class AutomationsEngine(Generic[_M]):
    _hub: Slot[_M, AutomationProperties[_M]]

    def __init__(
        self,
        ddl: 'DDL',
        crud: _Contract_CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        self._ddl = ddl
        # Inicialización de centro de automatización
        self._hub = Slot[_M, AutomationProperties[_M]]()

        # Inicialización de automatizaciones predeterminadas
        self._default_on_create_automations: EngineHub[_M, AutomationProperties[_M]] = DEFAULT_ON_CREATE_AUTOMATIONS
        self._default_on_update_automations: EngineHub[_M, AutomationProperties[_M]] = {}
        self._default_on_delete_automations: EngineHub[_M, AutomationProperties[_M]] = {}

    def build_hub(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:

        # Iteración por cada modelo de la base de datos
        for model_name in database_metadata.model_names:
            # Inicialización de centros de automatizaciones en cada tipo de transacción
            self._hub.create[model_name] = {}
            self._hub.update[model_name] = {}
            self._hub.delete[model_name] = {}

        # Inicialización de automatizaciones en cada uno de los tipos de transacción
        self._initialize_transaction_hub(self._default_on_create_automations, self._hub.create)
        self._initialize_transaction_hub(self._default_on_update_automations, self._hub.update)
        self._initialize_transaction_hub(self._default_on_delete_automations, self._hub.delete)

    def initialize_default_automations(
        self,
    ) -> None:

        # Inicialización de automatizaciones en cada uno de los tipos de transacción
        self._initialize_transaction_hub(self._default_on_create_automations, self._hub.create)
        self._initialize_transaction_hub(self._default_on_update_automations, self._hub.update)
        self._initialize_transaction_hub(self._default_on_delete_automations, self._hub.delete)

    def register(
        self,
        on: DMLTransaction,
        model_name: ModelName[_M],
        fields: list[FieldReadDeclaration] = [FIELD_NAME.ID],
        execute_only_when: CriteriaStructure = [],
    ) -> FunctionDecorator[AutomationCallback[_M]]:

        # Inicialización de decorador para obtener la función a registrar
        def decorator(callback: AutomationCallback[_M]) -> None:

            # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
            replaced_function = self._build_void_function()

            # Registro de la automatización
            self._register_automation(
                on,
                callback,
                model_name,
                fields,
                execute_only_when,
            )

            return replaced_function

        return decorator

    def execute_on_create(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
    ) -> None:

        # Obtención de diccionario de automatizaciones del modelo
        model_automations = self._hub.create.get(model_name)
        # Si no existen automatizaciones...
        if model_automations is None:
            # Se termina la ejecución
            return

        # Obtención de los campos a leer
        for ( automation_name, automation_properties ) in model_automations.items():

            # Inicialización de criterio de búsqueda
            search_criteria: CriteriaStructure = [(FIELD_NAME.ID, 'in', record_ids)]

            # Si las propiedades de automatización contienen un criterio de búsqueda...
            if automation_properties.execute_only_when:
                # Se añade éste
                search_criteria = ['&', *search_criteria, *automation_properties.execute_only_when ]

            # Lectura de los datos
            records_data = self._crud.search_read(execution_ctx, model_name, search_criteria, automation_properties.fields)

            # Si no existen resultados...
            if not records_data:
                # No se ejecuta la automatización
                continue

            # Inicialziación de contexto de automatización
            automation_ctx = AutomationContext(
                records_data,
                execution_ctx,
                self._crud,
                self._ddl,
            )

            # Ejecución de la función de automatización
            automation_properties.callback(automation_ctx)

    def execute_on_update(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
    ) -> None:

        # Obtención de diccionario de automatizaciones del modelo
        model_automations = self._hub.update.get(model_name)
        # Si no existen automatizaciones...
        if model_automations is None:
            # Se termina la ejecución
            return

        # Obtención de los campos a leer
        for ( automation_name, automation_properties ) in model_automations.items():

            # Inicialización de criterio de búsqueda
            condition: CriteriaStructure = [(FIELD_NAME.ID, 'in', record_ids)]

            # Si las propiedades de automatización contienen un criterio de búsqueda...
            if automation_properties.execute_only_when:
                # Se añade éste
                search_criteria = ['&', *search_criteria, *automation_properties.execute_only_when ]

            # Lectura de los datos
            records_data = self._crud.search_read(execution_ctx, model_name, condition, automation_properties.fields)

            # Si no existen resultados...
            if not records_data:
                # No se ejecuta la automatización
                continue

            # Inicialziación de contexto de automatización
            automation_ctx = AutomationContext(
                records_data,
                execution_ctx,
                self._crud,
                self._ddl,
            )

            # Ejecución de la función de automatización
            automation_properties.callback(automation_ctx)

    def prepare_on_delete(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        record_ids: list[int],
    ) -> CaptureIDsAfterDeletionFn:

        # Obtención de diccionario de automatizaciones del modelo
        model_automations = self._hub.delete.get(model_name)
        # Si no existen automatizaciones...
        if model_automations is None:
            # Inicialización de función vacía
            def execute_on_delete():
                ...
            return execute_on_delete

        # Inicialización de lista de automatizaciones a ejecutar
        automations_to_execute: list[Callable[[], None]] = []

        # Obtención de los campos a leer
        for ( automation_name, automation_properties ) in model_automations.items():

            # Inicialización de criterio de búsqueda
            condition: CriteriaStructure = [(FIELD_NAME.ID, 'in', record_ids)]

            # Si las propiedades de automatización contienen un criterio de búsqueda...
            if automation_properties.execute_only_when:
                # Se añade éste
                search_criteria = ['&', *search_criteria, *automation_properties.execute_only_when ]

            # Lectura de los datos
            records_data = self._crud.search_read(execution_ctx, model_name, condition, automation_properties.fields)

            # Si no existen resultados...
            if not records_data:
                # Se continúa con la siguiente automatización
                continue

            # Se obtienen los registros eliminados
            deleted_data = [record for record in records_data if record[FIELD_NAME.ID] in record_ids]

            # Inicialziación de contexto de automatización
            automation_ctx = AutomationContext(
                deleted_data,
                execution_ctx,
                self._crud,
                self._ddl,
            )

            # Inicialización de automatización a ejecutar
            automation_post_execute: lambda : automation_properties.callback(automation_ctx)

            # Se añade la automatización a la lista de automatizaciones por ejecutar
            automations_to_execute.append(automation_post_execute)

        # Inicialización de función para ejecutar tras la eliminación de registros
        def execute_on_delete():

            # Iteración por cada automatización a ejecutar
            for automation in automations_to_execute:
                # Ejecución de la automatización
                automation()

        return execute_on_delete

    def add(
        self,
        model_name: ModelName[_M],
    ) -> None:

        # Inicialización de diccionario de registros en cada una de las transacciones
        self._hub.create[model_name] = {}
        self._hub.update[model_name] = {}
        self._hub.delete[model_name] = {}

        # Si existen automatizaciones predeterminadas en creación...
        if model_name in DEFAULT_ON_CREATE_AUTOMATIONS:
            # Iteración por los datos
            for ( automation_name, automation_properties ) in DEFAULT_ON_CREATE_AUTOMATIONS[model_name].items():
                # Se añade la automatización
                self._hub.create[model_name][automation_name] = automation_properties

    def _register_automation(
        self,
        on: DMLTransaction,
        callback: AutomationCallback[_M],
        model_name: ModelName[_M],
        fields: list[FieldReadDeclaration] = [FIELD_NAME.ID],
        execute_only_when: CriteriaStructure = [],
    ) -> None:

        # Obtención del centro de automatizaciones del tipo de transacción
        hub = self._hub[on]

        # Inicialización de las propiedades de la automatización
        automation_properties = AutomationProperties[_M](
            callback= callback,
            model_name= model_name,
            fields= tuple(fields),
            execute_only_when= execute_only_when,
        )

        # Obtención del nombre de la función a registrar
        callback_name = callback.__name__

        # Registro de la automatización en el centro de automatizaciones
        hub[model_name][callback_name] = automation_properties

    def _build_void_function(
        self,
    ) -> AutomationCallback[_M]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(ctx: AutomationContext[_M]) -> None:
            # Se lanza error de ejecución
            raise AutomationExecutionError(ERROR_LABEL.MANUAL_AUTOMATION)

        return void_function

    def _initialize_transaction_hub(
        self,
        automations_to_add: EngineHub[_M, AutomationProperties[_M]],
        owned_hub: EngineHub[_M, AutomationProperties[_M]],
    ) -> None:

        # Iteración por nombre de modelo y automatizaciones de cada diccionario
        for ( model_name, automations ) in automations_to_add.items():

            # Si el nombre del modelo no existe en el centro de automatizaciones...
            if model_name not in owned_hub:
                # Se inicializa el diccionario de automatizaciones para el modelo
                owned_hub[model_name] = {}

            # Iteración por cada nombre de automatización y sus propiedades
            for ( automation_name, automation_properties ) in automations.items():

                # Se añaden las propiedades de la automatización al centro de automatizaciones
                owned_hub[model_name][automation_name] = automation_properties
