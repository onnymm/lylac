from ..._module_types import AutomationDataDict

preset_automations: list[AutomationDataDict] = [
    # Creación de tabla en base de datos cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_table',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field.selection', 'base.users'])],
        'fields': ['name', 'model'],
        'execution': 'record',
    },
    # Registro de modelo de SQLAlchemy cuando un modelo de crea
    {
        'submodule': '_automations',
        'callback': 'register_new_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field', 'base.users'])],
        'fields': ['model'],
        'execution': 'record',
    },
    # Creación de los registros de campos base cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_base_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field', 'base.users'])],
        'fields': [],
        'execution': 'record',
    },
    # Creación de los registros de campos predeterminados cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'add_preset_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field.selection', 'base.users'])],
        'fields': [],
        'execution': 'record',
    },
    # Eliminación de una tabla de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_table',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [('model', 'not in', ['base.model', 'base.model.field', 'base.model.field', 'base.users'])],
        'fields': ['name', 'model'],
        'execution': 'record',
    },
    # Creación de una columna de base de datos cuando un campo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_column',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '&',
                ('id', '>', 39),
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
    # Eliminación de una columna de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_column',
        'model': 'base.model.field',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['name', 'model_id'],
        'execution': 'record',
    },
]
