from ..._module_types import NewRecord
from ..._constants import BASE_USERS_MODEL_ID

DEFAULT_FIELD_TEMPLATE: dict[str, NewRecord.ModelField] = {
    'create_uid': {
        'label': 'Creado por',
        'name': 'create_uid',
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': BASE_USERS_MODEL_ID,
    },
    'write_uid': {
        'label': 'Modificado por',
        'name': 'write_uid',
        'ttype': 'many2one',
        'nullable': True,
        'related_model_id': BASE_USERS_MODEL_ID,
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
        'related_model_id': BASE_USERS_MODEL_ID,
    },
}

UID_FIELDS = ['create_uid', 'write_uid']
