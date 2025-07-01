from ..._module_types import FieldProperties

fields_atts: dict[str, dict[str, FieldProperties]] = {
    'base.model': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'model': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'label': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'description': {
            'ttype': 'text',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'state': {
            'ttype': 'selection',
            'related_model': None,
            'related_field': None,
            'selection_values': [
                'base',
                'generic',
            ],
        },
        'field_ids': {
            'ttype': 'one2many',
            'related_model': 'base.model.field',
            'related_field': 'model_id',
            'selection_values': [],
        },
        'related_field_ids': {
            'ttype': 'one2many',
            'related_model': 'base.model.field',
            'related_field': 'related_model_id',
            'selection_values': [],
        },
    },
    'base.model.field': {
        'id': {
            'ttype': 'integer',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'name': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'create_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'write_date': {
            'ttype': 'datetime',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'model_id': {
            'ttype': 'many2one',
            'related_model': 'base.model',
            'related_field': None,
            'selection_values': [],
        },
        'label': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'ttype': {
            'ttype': 'selection',
            'related_model': None,
            'related_field': None,
            'selection_values': [
                'integer',
                'char',
                'float',
                'boolean',
                'date',
                'datetime',
                'time',
                'file',
                'text',
                'selection',
                'many2one',
                'one2many',
                'many2many',
            ],
        },
        'nullable': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'is_required': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'default_value': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'unique': {
            'ttype': 'boolean',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'help_info': {
            'ttype': 'text',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'related_model_id': {
            'ttype': 'many2one',
            'related_model': 'base.model',
            'related_field': None,
            'selection_values': [],
        },
        'related_field': {
            'ttype': 'char',
            'related_model': None,
            'related_field': None,
            'selection_values': [],
        },
        'state': {
            'ttype': 'selection',
            'related_model': None,
            'related_field': None,
            'selection_values': [
                'base',
                'generic',
            ],
        },
        'selection_ids': {
            'ttype': 'one2many',
            'related_model': 'base.model.field.selection',
            'related_field': 'field_id',
            'selection_values': [],
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