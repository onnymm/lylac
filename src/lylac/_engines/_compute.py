from typing import Generic
from typing import TYPE_CHECKING
from .._contracts import _Contract_CRUD
from .._contracts.engines import Contract_ComputationEngine
from .._contracts.contexts import Contract_ExecutionContext
from .._data import DEFAULT_COMPUTATION_CALLBACKS
from .._resources import DatabaseMetadata
from .._typing.generics import ModelName
from .._typing.literals import TTypeName
from .._typing.structures import ComputeContextHub
from .._typing.type_parameters import _M

if TYPE_CHECKING:
    from .._typing.callables import CaptureComputeCallback
    from .._typing.callables import ComputeFieldFn

class ComputeEngine(Generic[_M], Contract_ComputationEngine[_M]):
    _presets: ComputeContextHub[_M] = DEFAULT_COMPUTATION_CALLBACKS

    def __init__(
        self,
    ) -> None:

        # Inicialización de centro de funciones de campos computados
        self.hub = {
            'base.users': {},
            'base.user.session': {},
            'base.model': {},
            'base.model.data': {},
            'base.model.data.process': {},
            'base.model.data.process.step': {},
            'base.model.data.process.step.record': {},
            'base.model.field': {},
            'base.model.field.selection': {},
        }

        # Iteración por cada modelo y su diccionario de funciones predeterminadas
        for ( model_name_i, funcs_dict_i ) in self._presets.items():
            # Iteración por cada nombre de campo y su función de cómputo
            for ( field_name, compute_callback ) in funcs_dict_i.items():
                # Asignación de función
                self.hub[model_name_i][field_name] = compute_callback

    def expand_to_custom_models(
        self,
        database_metadata: DatabaseMetadata[_M],
    ) -> None:

        # Iteración por cada nombre de modelo existente en la base de datos
        for model_name_i in database_metadata.model_names:
            # Si el nombre del modelo no está en el centro de campos computados...
            if model_name_i not in self.hub:
                # Inicialización de diccionario de campos computados del modelo i
                self.hub[model_name_i] = {}

    def register_field(
        self,
        crud: _Contract_CRUD[_M],
        execution_ctx: Contract_ExecutionContext[_M],
        model_name: ModelName[_M],
        name: str,
        label: str,
        ttype: TTypeName,
    ) -> CaptureComputeCallback[_M]:

        # Búsqueda del campo
        found_results = crud.search_count(
            execution_ctx,
            'base.model.field',
            [
                '&',
                    ('name', '=', name),
                    ('model_id.model', '=', model_name),
            ]
        )

        if not found_results:
            crud.create(
                execution_ctx,
                'base.model.field',
                {
                    'name': name,
                    'label': label,
                    'ttype': ttype,
                    'model_id': execution_ctx.get_resource_id(f'base_model.{model_name.replace('.', '_')}'),
                    'is_computed': True,
                }
            )

        def decorator(computation_callback: ComputeFieldFn[_M]):

            self.hub[model_name][name] = computation_callback

            return computation_callback

        return decorator

    def add(
        self,
        model_name: ModelName[_M],
    ) -> None:

        self.hub[model_name] = {}
