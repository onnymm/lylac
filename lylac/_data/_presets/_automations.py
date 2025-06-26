from ..._module_types import AutomationData

preset_automations: list[AutomationData] = [
    # Creación de tabla en base de datos cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_table',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['name', 'model'],
        'method': 'record',
    },
    # Registro de modelo de SQLAlchemy cuando un modelo de crea
    {
        'submodule': '_automations',
        'callback': 'register_new_model',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['model'],
        'method': 'record',
    },
    # Creación de los registros de campos base cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_base_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['id'],
        'method': 'record',
    },
    # Creación de los registros de campos predeterminados cuando un modelo se crea
    {
        'submodule': '_ddl',
        'callback': 'add_preset_fields',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [('state', '!=', 'base')],
        'fields': ['id'],
        'method': 'record',
    },
    # Inicialización de registro de validaciones de modelo cuando un modelo se crea
    {
        'submodule': '_validations',
        'callback': 'initialize_validations',
        'model': 'base.model',
        'transaction': 'create',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
    # Eliminación de una tabla de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_table',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [('state', '!=', 'base')],
        'fields': ['name', 'model'],
        'method': 'record',
    },
    # Creación de una columna de base de datos cuando un campo se crea
    {
        'submodule': '_ddl',
        'callback': 'create_column',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '&',
                ('state', '!=', 'base'),
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
        'method': 'record',
    },
    # Registro de las propiedades de campo cuando un campo se crea
    {
        'submodule': '_strc',
        'callback': 'register_field_atts',
        'model': 'base.model.field',
        'transaction': 'create',
        'criteria': [
            '|',
                ('name', 'in', ['create_uid', 'write_uid']),
                ('state', '!=', 'base'),
        ],
        'fields': [
            'name',
            'ttype',
            'model_id',
            'related_model_id',
            'related_field',
        ],
        'method': 'record',
    },
    # Eliminación de una columna de base de datos cuando un modelo se elimina
    {
        'submodule': '_ddl',
        'callback': 'delete_column',
        'model': 'base.model.field',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['name', 'model_id'],
        'method': 'record',
    },
    # Eliminación de registro de validaciones de modelo cuando un modelo se elimina
    {
        'submodule': '_validations',
        'callback': 'delete_validations',
        'model': 'base.model',
        'transaction': 'delete',
        'criteria': [],
        'fields': ['model'],
        'method': 'record',
    },
]
