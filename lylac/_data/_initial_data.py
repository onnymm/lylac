from .._models import (
    BaseModel_,
    BaseModelField,
    BaseModelFieldSelection,
)
from .._module_types import (
    NewModel,
    NewModelField,
    NewModelFieldSelection,
)

_base_model: list[NewModel] = [
    {
        'model': 'base.model',
        'name': 'base_model',
        'label': 'Modelos',
        'description': 'Este modelo define los modelos de la base de datos.',
    },
    {
        'model': 'base.model.field',
        'name': 'base_model_field',
        'label': 'Campos',
        'description': 'Este modelo define los campos de la base de datos.'
    },
    {
        'model': 'base.model.field.selection',
        'name': 'base_model_field_selection',
        'label': 'Tipo de selección',
        'description': 'Este modelo define los valores de selección para usarse como tipo de dato en campos de modelos.',
    },
]

_model_model_field: list[NewModelField] = [
    {
        'name': 'id',
        'label': 'ID',
        'ttype': 'integer',
        'model_id': 1,
        'nullable': False,
        'unique': True,
    },
    {
        'name': 'name',
        'label': 'Nombre',
        'ttype': 'char',
        'model_id': 1,
        'nullable': False,
    },
    {
        'name': 'create_date',
        'label': 'Fecha de creación',
        'ttype': 'datetime',
        'model_id': 1,
        'nullable': False,
    },
    {
        'name': 'write_date',
        'label': 'Fecha de modificación',
        'ttype': 'datetime',
        'model_id': 1,
        'nullable': False,
    },
    {
        'name': 'model',
        'label': 'Modelo',
        'ttype': 'char',
        'model_id': 1,
        'nullable': False,
        'unique': True,
    },
    {
        'name': 'label',
        'label': 'Etiqueta',
        'ttype': 'char',
        'model_id': 1,
        'nullable': False,
    },
    {
        'name': 'description',
        'label': 'Descripción',
        'ttype': 'text',
        'model_id': 1,
    },
    {
        'name': 'id',
        'label': 'ID',
        'ttype': 'integer',
        'model_id': 2,
        'nullable': False,
        'unique': True,
    },
    {
        'name': 'name',
        'label': 'Nombre',
        'ttype': 'char',
        'model_id': 2,
        'nullable': False,
    },
    {
        'name': 'create_date',
        'label': 'Fecha de creación',
        'ttype': 'datetime',
        'model_id': 2,
        'nullable': False,
    },
    {
        'name': 'write_date',
        'label': 'Fecha de modificación',
        'ttype': 'datetime',
        'model_id': 2,
        'nullable': False,
    },
    {
        'name': 'model_id',
        'label': 'Modelo',
        'ttype': 'integer',
        'model_id': 2,
        'nullable': False,
    },
    {
        'name': 'label',
        'label': 'Etiqueta de campo',
        'ttype': 'char',
        'model_id': 2,
        'nullable': False,
        'unique': True,
    },
    {
        'name': 'ttype',
        'label': 'Tipo',
        'ttype': 'selection',
        'model_id': 2,
        'nullable': False,
    },
    {
        'name': 'nullable',
        'label': 'Nulo',
        'ttype': 'boolean',
        'model_id': 2,
        'default_value': False,
    },
    {
        'name': 'is_required',
        'label': 'Requerido',
        'ttype': 'boolean',
        'model_id': 2,
        'default_value': False,
    },
    {
        'name': 'default_value',
        'label': 'Valor prestablecido',
        'ttype': 'char',
        'model_id': 2,
    },
    {
        'name': 'unique',
        'label': 'Es valor único',
        'ttype': 'boolean',
        'model_id': 2,
        'default_value': False,
    },
    {
        'name': 'related_model_id',
        'label': 'Modelo de relación',
        'ttype': 'integer',
        'model_id': 2,
    },
    {
        'name': 'selection_ids',
        'label': 'Valores de selección',
        'ttype': 'one2many',
        'model_id': 2,
    },
    {
        'name': 'id',
        'label': 'ID',
        'ttype': 'integer',
        'model_id': 3,
        'nullable': False,
        'unique': True,
    },
    {
        'name': 'name',
        'label': 'Nombre',
        'ttype': 'char',
        'model_id': 3,
        'nullable': False,
    },
    {
        'name': 'create_date',
        'label': 'Fecha de creación',
        'ttype': 'datetime',
        'model_id': 3,
        'nullable': False,
    },
    {
        'name': 'write_date',
        'label': 'Fecha de modificación',
        'ttype': 'datetime',
        'model_id': 3,
        'nullable': False,
    },
    {
        'name': 'label',
        'label': 'Etiqueta',
        'ttype': 'char',
        'model_id': 3,
    },
    {
        'name': 'field_id',
        'label': 'Campo',
        'ttype': 'many2one',
        'model_id': 3,
        'related_model_id': 2,
    },
]

_base_model_field_selection: list[NewModelFieldSelection] = [
    {
        'name': 'integer',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'char',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'float',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'boolean',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'date',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'datetime',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'time',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'file',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'text',
        'field_id': 14,
        'label': '',
    },
    {
        'name': 'selection',
        'field_id': 14,
        'label': '',
    },
]

initial_models = {
    'base.model': _base_model,
    'base.model.field': _model_model_field,
    'base.model.field.selection': _base_model_field_selection
}

# initial_models = {
#     BaseModel_: _base_model,
#     BaseModelField: _model_model_field,
#     BaseModelFieldSelection: _base_model_field_selection
# }
