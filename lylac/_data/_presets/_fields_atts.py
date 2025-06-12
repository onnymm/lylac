from ..._module_types import FieldProperties

fields_atts: dict[str, dict[str, FieldProperties]] = {
    'base.model': {
        'id': {
            'ttype': 'integer',
            'relation': None,
        },
        'name': {
            'ttype': 'char',
            'relation': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'model': {
            'ttype': 'char',
            'relation': None,
        },
        'label': {
            'ttype': 'char',
            'relation': None,
        },
        'description': {
            'ttype': 'text',
            'relation': None,
        },
    },
    'base.model.field': {
        'id': {
            'ttype': 'integer',
            'relation': None,
        },
        'name': {
            'ttype': 'char',
            'relation': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'model_id': {
            'ttype': 'many2one',
            'relation': 'base.model',
        },
        'label': {
            'ttype': 'char',
            'relation': None,
        },
        'ttype': {
            'ttype': 'selection',
            'relation': None,
        },
        'nullable': {
            'ttype': 'boolean',
            'relation': None,
        },
        'is_required': {
            'ttype': 'boolean',
            'relation': None,
        },
        'default_value': {
            'ttype': 'char',
            'relation': None,
        },
        'unique': {
            'ttype': 'boolean',
            'relation': None,
        },
        'help_info': {
            'ttype': 'text',
            'relation': None,
        },
        'related_model_id': {
            'ttype': 'many2one',
            'relation': 'base.model.field',
        },
    },
    'base.model.field.selection': {
        'id': {
            'ttype': 'integer',
            'relation': None,
        },
        'name': {
            'ttype': 'char',
            'relation': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'label': {
            'ttype': 'char',
            'relation': None,
        },
        'field_id': {
            'ttype': 'many2one',
            'relation': 'base.model.field',
        },
    },
    'base.users': {
        'id': {
            'ttype': 'integer',
            'relation': None,
        },
        'name': {
            'ttype': 'char',
            'relation': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'relation': None,
        },
        'login': {
            'ttype': 'char',
            'relation': None,
        },
        'password': {
            'ttype': 'char',
            'relation': None,
        },
        'odoo_id': {
            'ttype': 'integer',
            'relation': None,
        },
        'active': {
            'ttype': 'boolean',
            'relation': None,
        },
        'sync': {
            'ttype': 'boolean',
            'relation': None,
        },
    },
}