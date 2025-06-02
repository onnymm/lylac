from ..._module_types import NewModelField

base_fields: list[NewModelField] = [
    {
        'name': 'id',
        'label': 'ID',
        'ttype': 'integer',
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
]
