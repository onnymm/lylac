from ..._module_types import NewRecord

default_field_template: dict[str, NewRecord.ModelField] = {
    'create_uid': {
        'label': 'Creado por',
        'name': 'create_uid',
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': 4,
    },
    'write_uid': {
        'label': 'Modificado por',
        'name': 'write_uid',
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': 4,
    },
    'sequence': {
        'label': 'Secuencia',
        'name': 'sequence',
        'ttype': 'integer',
    },
    'user_id': {
        'label': 'Usuario',
        'name': 'user_id',
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': 4,
    },
}
