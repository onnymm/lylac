from ..._module_types import FieldProperties

fields_atts: dict[str, dict[str, FieldProperties]] = {
    'base.model': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'model': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'label': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'description': {
            'ttype': 'text',
            'related_model': None,
            'related_field': None,
        },
    },
    'base.model.field': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'model_id': {
            'ttype': 'many2one',
            'related_model': 'base.model',
            'related_field': None,
        },
        'label': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'ttype': {
            'ttype': 'selection',
            'related_model': None,
            'related_field': None,
        },
        'nullable': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
        },
        'is_required': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
        },
        'default_value': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'unique': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
        },
        'help_info': {
            'ttype': 'text',
            'related_model': None,
            'related_field': None,
        },
        'related_model_id': {
            'ttype': 'many2one',
            'related_model': 'base.model.field',
            'related_field': None,
        },
        'state': {
            'ttype': 'selection',
            'related_model': None,
            'related_field': None,
        },
    },
    'base.model.field.selection': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'label': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'field_id': {
            'ttype': 'many2one',
            'related_model': 'base.model.field',
            'related_field': None,
        },
    },
    'base.users': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
        },
        'login': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'password': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
        },
        'odoo_id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
        },
        'active': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
        },
        'sync': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
        },
    },
}