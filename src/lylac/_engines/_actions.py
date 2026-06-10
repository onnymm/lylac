from typing import Generic
from typing import Literal
from typing import TYPE_CHECKING
from .._constants import ERROR_LABEL
from .._contexts import ActionContext as _ActionContext
from .._contracts.contexts import Contract_ExecutionContext
from .._contracts import _Contract_CRUD
from .._data import PRESET_ACTIONS
from .._resources import ActionProperties
from .._resources import DatabaseMetadata
from .._typing.callables import ActionCallback
from .._typing.generics import EngineHub
from .._typing.generics import FunctionDecorator
from .._typing.generics import ModelName
from .._typing.type_parameters import _M
from ..errors import ActionExecutionError

if TYPE_CHECKING:
    from .._operations import DDL

class ActionEngine(Generic[_M]):

    def __init__(
        self,
        ddl: DDL[_M],
        crud: _Contract_CRUD[_M],
    ) -> None:

        # Asignación de valores
        self._crud = crud
        self._ddl = ddl
        # Inicialización de centro de acciones
        self._hub: EngineHub[_M, ActionProperties[_M]] = {}

    def build_hub(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:

        # Iteración por cada modelo de la base de datos
        for model_name in database_metadata.model_names:
            # Inicialización de diccionario de acciones
            self._hub[model_name] = {}

        # Iteración por cada modelo que contiene acciones predeterminadas
        for model_name in PRESET_ACTIONS:
            # Iteración por cada acción
            for ( action_name, action_properties ) in PRESET_ACTIONS[model_name].items():
                # Registro en el centro de acciones
                self._hub[model_name][action_name] = action_properties

    def register(
        self,
        model_name: ModelName[_M],
        name: str,
        fields: list[str] = [],
    ) -> FunctionDecorator[ActionCallback[_M]]:

        # Inicialización de decorador para obtener la función a registrar
        def decorator(callback: ActionCallback[_M]):

            # Registro de la función de acción
            self._register_action(
                model_name,
                name,
                callback,
                fields,
            )

            # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
            replaced_function = self._build_void_function()

            return replaced_function

        return decorator

    def execute(
        self,
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        name: str,
        record_id: int,
    ) -> Literal[True]:

        # Obtención de las propiedades de la automatización
        automation_properties = self._hub[model_name][name]
        # Obtención de la función
        callback = automation_properties.callback
        # Obtención de los campos a leer
        fields_to_read = list(automation_properties.fields)

        # Lectura del registro
        [ record ] = self._crud.read(
            execution_ctx,
            model_name,
            record_id,
            fields_to_read,
        )

        # Inicialización de contexto de automatización
        ctx = _ActionContext[_M](execution_ctx, self._crud, record, self._ddl)

        # Ejecución de la acción
        callback(ctx)

    def add(
        self,
        model_name: ModelName[_M],
    ) -> None:

        # Inicialización de diccionario en el modelo
        self._hub[model_name] = {}

    def _register_action(
        self,
        model_name: ModelName[_M],
        name: str,
        callback: ActionCallback[_M],
        fields: list[str],
    ) -> None:

        # Inicialización de instancia de propiedades de acción
        action_properties = ActionProperties(
            model_name,
            callback,
            tuple(fields),
        )

        # Registro de las propiedades
        self._hub[model_name][name] = action_properties

    def _build_void_function(
        self,
    ) -> FunctionDecorator[ActionCallback[_M]]:

        # Inicialización de función de reemplazo para arrojar error cuando se intente ejecutar manualmente
        def void_function(ctx: ActionCallback[_M]) -> None:
            # Se lanza error de ejecución
            raise ActionExecutionError(ERROR_LABEL.MANUAL_ACTION)

        return void_function
