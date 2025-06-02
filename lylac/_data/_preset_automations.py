from .._module_types import AutomationDataDict

preset_automations: list[AutomationDataDict] = [
    {
        'submodule': '_ddl',
        'callback': 'create_table',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field'])],
        'fields': ['name', 'model'],
        'execution': 'record',
    },
    {
        'submodule': '_automations',
        'callback': 'register_new_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field'])],
        'fields': ['model'],
        'execution': 'record',
    },
    {
        'submodule': '_ddl',
        'callback': 'delete_table',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field'])],
        'fields': ['name', 'model'],
        'execution': 'record',
    },
    {
        'submodule': '_ddl',
        'callback': 'create_column',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '&',
                ('id', '>', 26),
                ('name', 'not in', ['id', 'name', 'create_date', 'write_date'])
        ],
        'fields': [
            'name',
            'model_id',
            'label',
            'ttype',
            'nullable',
            'is_required',
            'unique',
            'default_value',
            'help_info',
            'related_model_id'
        ],
        'execution': 'record',
    },
    {
        'submodule': '_ddl',
        'callback': 'create_base_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field'])],
        'fields': [],
        'execution': 'record',
    },
    {
        'submodule': '_ddl',
        'callback': 'delete_column',
        'model': 'base.model.field',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['name', 'model_id'],
        'execution': 'record',
    }
]
