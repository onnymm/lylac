from typing import TYPE_CHECKING
from .._resources import ActionProperties
from .._typing.generics import EngineHub
from .._typing.type_parameters import _M
from .._typing.generics import ModelName

if TYPE_CHECKING:
    from .._contexts import ActionContext

def _base_model__create_model(ctx: ActionContext):

    # Obtención del nombre de modelo
    table_name = ctx.data['name']
    # Obtención del modelo del modelo
    model_name = ctx.data['model']
    # Obtención de valor de si el modelo tiene secuencia
    has_sequence = ctx.data['has_sequence']
    # Obtención de valor de si el modelo permite archivar
    is_archivable = ctx.data['is_archivable']
    # Obtención de valor de si el modelo contiene leyenda
    has_label = ctx.data['has_label']

    # Creación de la clase del modelo
    ctx._ddl.create_model_table(ctx._execution_ctx.conn, table_name, model_name, has_sequence, is_archivable, has_label)

PRESET_ACTIONS: EngineHub[_M, ActionProperties[_M]] = {

    'base.model': {
        'create_model': ActionProperties(
            'base.model',
            'create_model',
            _base_model__create_model,
        ),
    },

}
